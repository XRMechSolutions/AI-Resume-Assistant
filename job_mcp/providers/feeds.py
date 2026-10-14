"""Public remote-job feeds that need no login. Whole-feed sources are cached, then filtered locally."""

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from ..models import Job
from .base import Found, Http, Provider, ProviderError, html_to_text, matches_query

_FEED_CACHE_S = 30 * 60


class Remotive(Provider):
    """API terms: jobs are for personal use here, never republished to other sites."""

    name, access = "remotive", "public"
    _API = "https://remotive.com/api/remote-jobs"

    def __init__(self, http: Http, category: str = ""):
        self._http = http
        self._category = category

    async def search(self, query: str, limit: int) -> Found:
        params = {"search": query, "limit": "100"}
        if self._category:
            params["category"] = self._category
        data = await self._http.json(self._API, params, cache_s=_FEED_CACHE_S)
        # Remotive's search is fuzzy (it returns office and sales roles for "python"), so filter locally too.
        return Found([
            Job(
                source=self.name, title=j["title"], company=j["company_name"].strip(), url=j["url"],
                location=j.get("candidate_required_location", ""), remote="remote",
                salary=j.get("salary", ""), posted=j.get("publication_date", ""),
            )
            for j in data.get("jobs", [])
            if matches_query(query, j.get("title", ""), " ".join(j.get("tags") or []), j.get("category", ""))
        ][:limit])


class RemoteOK(Provider):
    """API terms require crediting Remote OK and linking back; results keep the remoteok.com URL."""

    name, access = "remoteok", "public"
    _API = "https://remoteok.com/api"

    def __init__(self, http: Http):
        self._http = http

    async def search(self, query: str, limit: int) -> Found:
        data = await self._http.json(self._API, cache_s=_FEED_CACHE_S)
        jobs = []
        for j in data[1:]:  # element 0 is the legal notice
            tags = " ".join(j.get("tags") or [])
            if not matches_query(query, j.get("position", ""), tags):
                continue
            lo, hi = j.get("salary_min") or 0, j.get("salary_max") or 0
            jobs.append(Job(
                source=self.name, title=j["position"], company=j["company"], url=j["url"],
                location=j.get("location", ""), remote="remote",
                salary=f"${lo:,}-${hi:,}" if lo and hi else "", posted=j.get("date", ""),
                extra={"tags": tags},
            ))
        return Found(jobs[:limit])


class WeWorkRemotely(Provider):
    name, access = "weworkremotely", "public"
    _RSS = "https://weworkremotely.com/categories/{category}.rss"

    def __init__(self, http: Http, categories: list[str]):
        if not categories:
            raise ProviderError("weworkremotely: enabled but no categories listed in policy.yaml")
        self._http = http
        self._categories = categories

    async def search(self, query: str, limit: int) -> Found:
        jobs, warnings = [], []
        for cat in self._categories:
            try:
                resp = await self._http.get(self._RSS.format(category=cat))
                root = ET.fromstring(resp.content)
            except (ProviderError, ET.ParseError) as exc:
                warnings.append(f"{cat}: {exc}")
                continue
            for item in root.iter("item"):
                raw_title = item.findtext("title", "")
                company, _, title = raw_title.partition(": ")
                if not matches_query(query, raw_title, item.findtext("category", "")):
                    continue
                jobs.append(Job(
                    source=self.name, title=title or raw_title, company=company if title else "",
                    url=item.findtext("link", ""), location=item.findtext("region", ""), remote="remote",
                    posted=item.findtext("pubDate", ""),
                ))
        if warnings and len(warnings) == len(self._categories):
            raise ProviderError("; ".join(warnings))
        return Found(jobs[:limit], warnings)


class HackerNewsHiring(Provider):
    """Top-level comments in the latest 'Ask HN: Who is hiring?' thread, via the Algolia HN API."""

    name, access = "hn_hiring", "public"
    _API = "https://hn.algolia.com/api/v1"
    url_pattern = re.compile(r"news\.ycombinator\.com/item\?id=(\d+)")

    def __init__(self, http: Http):
        self._http = http

    async def _latest_story(self) -> str:
        data = await self._http.json(
            f"{self._API}/search_by_date", {"tags": "story,author_whoishiring", "hitsPerPage": "5"}, cache_s=_FEED_CACHE_S,
        )
        for hit in data.get("hits", []):
            if "who is hiring" in hit.get("title", "").lower():
                return hit["objectID"]
        raise ProviderError("hn_hiring: no recent 'Who is hiring?' thread found")

    async def search(self, query: str, limit: int) -> Found:
        story = await self._latest_story()
        data = await self._http.json(
            f"{self._API}/search", {"tags": f"comment,story_{story}", "query": query, "hitsPerPage": str(min(limit * 2, 100))},
        )
        jobs = []
        for hit in data.get("hits", []):
            if str(hit.get("parent_id")) != story:  # replies are discussion, not postings
                continue
            text = html_to_text(hit.get("comment_text", ""))
            head = text.split("\n", 1)[0]
            fields = [f.strip() for f in head.split("|")]
            jobs.append(Job(
                source=self.name, title=fields[1] if len(fields) > 1 else head[:120],
                company=fields[0][:80], url=f"https://news.ycombinator.com/item?id={hit['objectID']}",
                location=" | ".join(fields[2:])[:160], posted=hit.get("created_at", ""), summary=text[:500],
            ))
        return Found(jobs[:limit])

    def owns_url(self, url: str) -> bool:
        return bool(self.url_pattern.search(url))

    async def details(self, url: str) -> str:
        item = await self._http.json(f"{self._API}/items/{self.url_pattern.search(url).group(1)}")
        return html_to_text(item.get("text") or "")


class Himalayas(Provider):
    name, access = "himalayas", "public"
    _API = "https://himalayas.app/jobs/api/search"

    def __init__(self, http: Http):
        self._http = http

    async def search(self, query: str, limit: int) -> Found:
        data = await self._http.json(self._API, {"q": query, "limit": str(min(limit, 20))}, cache_s=_FEED_CACHE_S)
        jobs = []
        for j in data.get("jobs", []):
            lo, hi = j.get("minSalary"), j.get("maxSalary")
            places = j.get("locationRestrictions") or []
            pub = j.get("pubDate")
            jobs.append(Job(
                source=self.name, title=j["title"], company=j.get("companyName", ""),
                url=j.get("applicationLink") or j.get("guid", ""), remote="remote",
                location=", ".join(places[:6]) + (f" (+{len(places) - 6} more)" if len(places) > 6 else ""),
                salary=f"{j.get('currency', '')} {lo:,}-{hi:,}".strip() if lo and hi else "",
                posted=datetime.fromtimestamp(int(pub), timezone.utc).date().isoformat() if pub else "",
                summary=j.get("excerpt", ""),
            ))
        return Found(jobs[:limit])
