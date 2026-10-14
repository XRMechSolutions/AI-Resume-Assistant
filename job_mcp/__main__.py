"""Entry point.

  python -m job_mcp                 run the MCP server on stdio (what Claude Code launches)
  python -m job_mcp check           load policy.yaml and list sources (no network)
  python -m job_mcp login <source>  open a board's sign-in page; close the window when done
"""

import asyncio
import sys

from .browser.session import BrowserSession
from .config import ConfigError, load_config


def _check() -> int:
    from .pacing import Pacer
    from .providers import build_providers
    from .providers.base import Http

    cfg = load_config()

    async def build():
        http = Http(cfg.user_agent, Pacer(cfg.http_min_delay_s))
        try:
            return build_providers(cfg, http, BrowserSession(cfg))
        finally:
            await http.aclose()

    providers, errors = asyncio.run(build())
    for name, p in providers.items():
        print(f"  {name:16} {p.access}")
    for name, err in errors.items():
        print(f"  {name:16} NOT LOADED: {err}")
    print(f"profile: {cfg.profile_dir}")
    return 1 if errors else 0


def _login(source: str) -> int:
    cfg = load_config()
    src = cfg.sources.get(source)
    if not src or src.kind != "browser_board":
        print(f"'{source}' is not a browser_board source in policy.yaml", file=sys.stderr)
        return 2

    async def run():
        session = BrowserSession(cfg)
        await session.open(src.settings["login_url"])
        print(f"Sign in to {source} in the Chrome window, then close that window.")
        await session.wait_until_closed()
        await session.close()

    asyncio.run(run())
    return 0


def main() -> int:
    args = sys.argv[1:]
    try:
        if not args:
            from .server import mcp
            mcp.run()
            return 0
        if args == ["check"]:
            return _check()
        if len(args) == 2 and args[0] == "login":
            return _login(args[1])
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
