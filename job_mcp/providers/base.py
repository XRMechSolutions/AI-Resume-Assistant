"""Provider contract and the shared paced HTTP client."""

import html
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urlsplit

import httpx

from ..models import Job
from ..pacing import Pacer


class ProviderError(Exception):
    pass


class Http:
    """One client for every public source, spaced per host so no board sees bursts."""

    def __init__(self, user_agent: str, pacer: Pacer, transport: httpx.AsyncBaseTransport | None = None):
        self._client = httpx.AsyncClient(
            transport=transport,
            headers={"User-Agent": user_agent, "Accept": "application/json, application/rss+xml, */*"},
            timeout=httpx.Timeout(20.0, connect=10.0),
            follow_redirects=True,
        )
        self._pacer = pacer
        self._cache: dict[tuple, tuple[float, object]] = {}

    async def get(self, url: str, params: dict | None = None) -> httpx.Response:
        await self._pacer.wait(urlsplit(url).netloc)
        try:
            resp = await self._client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise ProviderError(f"{urlsplit(url).netloc}: {type(exc).__name__}: {exc}") from exc
        if resp.status_code != 200:
            raise ProviderError(f"{urlsplit(url).netloc} returned HTTP {resp.status_code}")
        return resp

    async def json(self, url: str, params: dict | None = None, cache_s: float = 0):
        """cache_s reuses a recent response; whole-feed sources ask boards to keep calls rare."""
        key = (url, tuple(sorted((params or {}).items())))
        hit = self._cache.get(key)
        if cache_s and hit and time.monotonic() - hit[0] < cache_s:
            return hit[1]
        resp = await self.get(url, params)
        try:
            data = resp.json()
        except ValueError as exc:
            raise ProviderError(f"{urlsplit(url).netloc} returned invalid JSON") from exc
        if cache_s:
            self._cache[key] = (time.monotonic(), data)
        return data

    async def aclose(self) -> None:
        await self._client.aclose()


class _TextExtractor(HTMLParser):
    _BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "section", "ul", "ol"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in self._BLOCK:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(markup: str) -> str:
    # Greenhouse double-escapes its content field, so unescape once before parsing.
    if "&lt;" in markup and "<" not in markup:
        markup = html.unescape(markup)
    parser = _TextExtractor()
    parser.feed(markup)
    text = "".join(parser.parts).replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def matches_query(query: str, *fields: str) -> bool:
    """Every word of the query must appear somewhere; quoted phrases count as one word."""
    haystack = " ".join(fields).lower()
    terms = re.findall(r'"([^"]+)"|(\S+)', query.lower())
    return all((a or b) in haystack for a, b in terms)


@dataclass
class Found:
    jobs: list[Job]
    warnings: list[str] = field(default_factory=list)


class Provider(ABC):
    name: str
    access: str  # "public" or "browser"

    @abstractmethod
    async def search(self, query: str, limit: int) -> Found: ...

    def owns_url(self, url: str) -> bool:
        return False

    async def details(self, url: str) -> str:
        raise ProviderError(f"{self.name} cannot fetch details for {url}")
