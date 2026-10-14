"""Builds the enabled providers from policy.yaml."""

from ..browser.session import BrowserSession
from ..config import Config
from .ats import Ashby, Greenhouse, Lever
from .base import Http, Provider, ProviderError
from .board import BrowserBoard
from .feeds import HackerNewsHiring, Himalayas, RemoteOK, Remotive, WeWorkRemotely


def build_providers(cfg: Config, http: Http, session: BrowserSession) -> tuple[dict[str, Provider], dict[str, str]]:
    """Returns (providers, config_errors). A misconfigured source is reported, not dropped silently."""
    makers = {
        "greenhouse": lambda n, s: Greenhouse(n, http, s.get("companies", [])),
        "lever": lambda n, s: Lever(n, http, s.get("companies", [])),
        "ashby": lambda n, s: Ashby(n, http, s.get("companies", [])),
        "remotive": lambda n, s: Remotive(http, s.get("category", "")),
        "remoteok": lambda n, s: RemoteOK(http),
        "weworkremotely": lambda n, s: WeWorkRemotely(http, s.get("categories", [])),
        "hn_hiring": lambda n, s: HackerNewsHiring(http),
        "himalayas": lambda n, s: Himalayas(http),
        "browser_board": lambda n, s: BrowserBoard(n, session, s),
    }
    providers, errors = {}, {}
    for name, src in cfg.sources.items():
        if not src.enabled:
            continue
        make = makers.get(src.kind)
        if make is None:
            errors[name] = f"unknown kind '{src.kind}'"
            continue
        try:
            providers[name] = make(name, src.settings)
        except ProviderError as exc:
            errors[name] = str(exc)
    return providers, errors
