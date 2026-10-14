"""Public job-board APIs of the three ATSes most target companies use: Greenhouse, Lever, Ashby.

Each reads a per-company board, so `companies` in policy.yaml decides coverage.
"""

import asyncio
import re
from datetime import datetime, timezone

from ..models import Job
from .base import Found, Http, Provider, ProviderError, html_to_text, matches_query


def _sortable_date(posted: str) -> str:
    """ISO strings sort correctly once reduced to UTC date-time; unknown dates sort last."""
    try:
        return datetime.fromisoformat(posted.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
    except ValueError:
        return ""


class _CompanyBoardProvider(Provider):
    access = "public"
    url_pattern: re.Pattern

    def __init__(self, name: str, http: Http, companies: list[str]):
        if not companies:
            raise ProviderError(f"{name}: enabled but no companies listed in policy.yaml")
        self.name = name
        self._http = http
        self._companies = companies

    async def _board(self, company: str) -> list[Job]: ...

    async def search(self, query: str, limit: int) -> Found:
        boards = await asyncio.gather(*(self._board(c) for c in self._companies), return_exceptions=True)
        jobs, failures = [], []
        for company, result in zip(self._companies, boards):
            if isinstance(result, BaseException):
                failures.append(f"{company}: {result}")
                continue
            jobs.extend(j for j in result if matches_query(query, j.title, j.location, j.extra.get("team", "")))
        if failures and len(failures) == len(self._companies):
            raise ProviderError("; ".join(failures))
        # Newest first across all companies: applying within days of posting is what gets responses.
        jobs.sort(key=lambda j: _sortable_date(j.posted), reverse=True)
        return Found(jobs[:limit], failures)

    def owns_url(self, url: str) -> bool:
        return bool(self.url_pattern.search(url))


class Greenhouse(_CompanyBoardProvider):
    url_pattern = re.compile(r"(?:job-boards|boards)\.greenhouse\.io/([\w-]+)/jobs/(\d+)")
    _API = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"

    async def _board(self, token: str) -> list[Job]:
        data = await self._http.json(self._API.format(token=token))
        return [
            Job(
                source=self.name,
                title=j["title"],
                company=j.get("company_name") or token,
                url=j["absolute_url"],
                location=(j.get("location") or {}).get("name", ""),
                posted=j.get("first_published") or j.get("updated_at", ""),
                extra={"team": ", ".join(d["name"] for d in j.get("departments", []))},
            )
            for j in data.get("jobs", [])
        ]

    async def details(self, url: str) -> str:
        m = self.url_pattern.search(url)
        data = await self._http.json(self._API.format(token=m.group(1)) + f"/{m.group(2)}")
        return html_to_text(data.get("content", ""))


class Lever(_CompanyBoardProvider):
    url_pattern = re.compile(r"jobs\.lever\.co/([\w-]+)/([0-9a-f-]{36})")
    _API = "https://api.lever.co/v0/postings/{company}"

    @staticmethod
    def _to_job(name: str, company: str, j: dict) -> Job:
        cats = j.get("categories") or {}
        created = j.get("createdAt")
        return Job(
            source=name,
            title=j["text"],
            company=company,
            url=j["hostedUrl"],
            location=cats.get("location", ""),
            remote=j.get("workplaceType", ""),
            posted=datetime.fromtimestamp(created / 1000, timezone.utc).date().isoformat() if created else "",
            extra={"team": cats.get("team", ""), "commitment": cats.get("commitment", "")},
        )

    async def _board(self, company: str) -> list[Job]:
        data = await self._http.json(self._API.format(company=company), {"mode": "json"})
        return [self._to_job(self.name, company, j) for j in data]

    async def details(self, url: str) -> str:
        m = self.url_pattern.search(url)
        j = await self._http.json(self._API.format(company=m.group(1)) + f"/{m.group(2)}", {"mode": "json"})
        lists = "\n\n".join(f"{x['text']}\n{html_to_text(x['content'])}" for x in j.get("lists", []))
        return "\n\n".join(p for p in (j.get("descriptionPlain", ""), lists, j.get("additionalPlain", "")) if p)


class Ashby(_CompanyBoardProvider):
    url_pattern = re.compile(r"jobs\.ashbyhq\.com/([\w.-]+)/([0-9a-f-]{36})")
    _API = "https://api.ashbyhq.com/posting-api/job-board/{org}"

    async def _raw(self, org: str) -> list[dict]:
        data = await self._http.json(self._API.format(org=org), {"includeCompensation": "true"})
        return [j for j in data.get("jobs", []) if j.get("isListed", True)]

    async def _board(self, org: str) -> list[Job]:
        jobs = []
        for j in await self._raw(org):
            comp = j.get("compensation") or {}
            jobs.append(Job(
                source=self.name,
                title=j["title"],
                company=org,
                url=j["jobUrl"],
                location=j.get("location", ""),
                remote="remote" if j.get("isRemote") else (j.get("workplaceType") or ""),
                salary=comp.get("compensationTierSummary") or "",
                posted=j.get("publishedAt", ""),
                extra={"team": j.get("team") or j.get("department") or ""},
            ))
        return jobs

    async def details(self, url: str) -> str:
        m = self.url_pattern.search(url)
        for j in await self._raw(m.group(1)):
            if j["id"] == m.group(2):
                return j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml", ""))
        raise ProviderError(f"Ashby board {m.group(1)} no longer lists job {m.group(2)} (closed or unlisted)")
