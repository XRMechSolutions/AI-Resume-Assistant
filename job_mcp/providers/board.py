"""Job boards searched through the logged-in browser, using each board's own search page.

Selectors are not used; a board is described in policy.yaml by its search URL and a regex for
job-posting links, which survives most redesigns. Zero matches is reported with sample links so
the pattern can be fixed rather than silently returning nothing.
"""

import re
from urllib.parse import quote_plus

from ..browser.session import BrowserSession
from ..models import Job
from .base import Found, Provider, ProviderError


class BrowserBoard(Provider):
    access = "browser"

    def __init__(self, name: str, session: BrowserSession, settings: dict):
        try:
            self._search_url = settings["search_url"]
            self._link_pattern = settings["job_link_pattern"]
            self._canonical = settings.get("canonical_url", "")
            self._page_size = int(settings.get("page_size", 25))
            self._max_pages = int(settings["max_pages_per_run"])
            self._logged_out = [m.lower() for m in settings.get("logged_out_url_markers", [])]
            self.login_url = settings["login_url"]
            self.cookie_domain = settings["cookie_domain"]
            self.session_cookie = settings.get("session_cookie", "")
            self.verified = bool(settings.get("verified", False))
        except KeyError as exc:
            raise ProviderError(f"{name}: policy.yaml is missing {exc}") from exc
        re.compile(self._link_pattern)
        self.name = name
        self._session = session

    def owns_url(self, url: str) -> bool:
        return bool(re.search(self._link_pattern, url))

    def _canonicalize(self, link: dict) -> str:
        if not self._canonical:
            return link["href"]
        groups = link["groups"]
        return re.sub(r"\{(\d+)\}", lambda m: groups[int(m.group(1))] or "", self._canonical)

    async def search(self, query: str, limit: int) -> Found:
        jobs: dict[str, Job] = {}
        for page_no in range(self._max_pages):
            url = self._search_url.format(query=quote_plus(query), page=page_no + 1, offset=page_no * self._page_size)
            landed = await self._session.open(url)
            if any(marker in landed["url"].lower() for marker in self._logged_out):
                raise ProviderError(f"{self.name}: not logged in (landed on {landed['url'][:80]}). "
                                    f"Run job_login('{self.name}') and sign in by hand.")
            await self._session.scroll_through()
            found = await self._session.links_matching(self._link_pattern, max_links=100)
            if not found["links"]:
                if page_no == 0 and not jobs:
                    raise ProviderError(
                        f"{self.name}: no links matched job_link_pattern on '{found['title']}' ({found['url'][:100]}). "
                        f"Sample links: {found['sample_hrefs'][:12]}. Fix the pattern in job_mcp/policy.yaml.")
                break
            before = len(jobs)
            for link in found["links"]:
                url = self._canonicalize(link)
                lines = [ln.strip() for ln in link["card"].split("\n") if ln.strip()]
                title = link["text"].split("\n")[0].strip() or (lines[0] if lines else "")
                rest = [ln for ln in lines if ln != title]
                jobs.setdefault(url, Job(
                    source=self.name, title=title, company=rest[0] if rest else "", url=url,
                    location=rest[1] if len(rest) > 1 else "", summary=" | ".join(rest[:6])[:400],
                ))
            if len(jobs) >= limit or len(jobs) == before:
                break
        return Found(list(jobs.values())[:limit],
                     [] if self.verified else [f"{self.name}: link pattern not yet confirmed on a live page; check titles"])

    async def details(self, url: str) -> str:
        await self._session.open(url)
        page = await self._session.read_text(0, 20_000)
        return page["text"]
