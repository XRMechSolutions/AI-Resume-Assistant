"""Normalized job record shared by every provider."""

import re
from dataclasses import asdict, dataclass, field
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_TRACKING_PARAMS = re.compile(r"^(utm_|ref$|refid$|trk|src$|source$|lever-|gh_src$|trackingid$)", re.I)


def normalize_url(url: str) -> str:
    """Canonical form used for duplicate checks across sources and CSVs."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    # LinkedIn serves the same posting from country subdomains (nl., de., es.).
    if host.endswith(".linkedin.com"):
        host = "www.linkedin.com"
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query) if not _TRACKING_PARAMS.match(k)))
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(("https", host, path, query, ""))


def title_key(company: str, title: str) -> str:
    squash = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return f"{squash(company)}|{squash(title)}"


@dataclass
class Job:
    source: str
    title: str
    company: str
    url: str
    location: str = ""
    remote: str = ""
    salary: str = ""
    posted: str = ""
    summary: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return normalize_url(self.url)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["key"] = self.key
        return d
