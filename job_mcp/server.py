"""MCP tools: discover jobs across boards, then walk an application up to (never through) Submit."""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP, Image
from mcp.server.fastmcp.exceptions import ToolError

from .browser.session import BrowserError, BrowserSession
from .config import Config, load_config
from .known_jobs import CsvError, append_to_queue, load_known
from .log import setup_logging
from .models import Job, normalize_url
from .pacing import Pacer
from .providers import build_providers
from .providers.base import Http, Provider, ProviderError
from .providers.board import BrowserBoard
from .store import MARKS, SeenStore

log = logging.getLogger("job_mcp.server")


@dataclass
class App:
    cfg: Config
    http: Http
    store: SeenStore
    browser: BrowserSession
    providers: dict[str, Provider]
    config_errors: dict[str, str]


@asynccontextmanager
async def lifespan(_server: FastMCP):
    cfg = load_config()
    setup_logging(cfg.log_path)
    http = Http(cfg.user_agent, Pacer(cfg.http_min_delay_s))
    store = SeenStore(cfg.state_dir / "seen.sqlite")
    browser = BrowserSession(cfg)
    providers, errors = build_providers(cfg, http, browser)
    for name, err in errors.items():
        log.warning("source %s not loaded: %s", name, err)
    try:
        yield App(cfg, http, store, browser, providers, errors)
    finally:
        await browser.close()
        await http.aclose()
        store.close()


mcp = FastMCP(
    "job-search",
    instructions=(
        "Job discovery and application prep for the user's job search in this repo. Search with job_search, "
        "read postings with job_details, queue keepers with queue_add. To apply: browser_open the posting, "
        "browser_form to list fields, fill them from the job's JobSearches/ folder, then browser_handoff. "
        "The final Submit is never clicked by these tools; the user reviews and submits. Every answer typed into a "
        "form must trace to the user's source of truth document (see CLAUDE.md)."
    ),
    lifespan=lifespan,
)


def _app(ctx: Context) -> App:
    return ctx.request_context.lifespan_context


def _compact(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in ("", None, {}, [])}


# ---------------------------------------------------------------- discovery


@mcp.tool()
async def job_sources(ctx: Context) -> dict:
    """List job sources, their access type, and whether each logged-in board has a session."""
    app = _app(ctx)
    out = []
    for name, p in app.providers.items():
        row = {"name": name, "access": p.access}
        if isinstance(p, BrowserBoard):
            row["verified_pattern"] = p.verified
            if p.session_cookie:
                try:
                    names = await app.browser.cookie_names(p.cookie_domain)
                except BrowserError as exc:
                    raise ToolError(str(exc)) from exc
                row["logged_in"] = p.session_cookie in names
            else:
                row["logged_in"] = "unknown: open the board with browser_open to check"
        out.append(row)
    return {"sources": out, "not_loaded": app.config_errors}


@mcp.tool()
async def job_login(source: str, ctx: Context) -> str:
    """Open a logged-in board's sign-in page in the job-search Chrome window so the user can log in by hand."""
    app = _app(ctx)
    p = app.providers.get(source)
    if not isinstance(p, BrowserBoard):
        raise ToolError(f"'{source}' is not an enabled browser board; see job_sources")
    try:
        await app.browser.open(p.login_url)
        await app.browser.bring_to_front()
    except BrowserError as exc:
        raise ToolError(str(exc)) from exc
    return (f"The {source} sign-in page is open in the job-search Chrome window. Ask the user to sign in there "
            "(including any 2FA), then call job_sources to confirm. The session is kept in the profile.")


def _pick(app: App, sources: list[str] | None) -> list[Provider]:
    if not sources:
        return [p for p in app.providers.values() if p.access == "public"]
    picked: dict[str, Provider] = {}
    for s in sources:
        if s in ("all", "public", "browser"):
            picked.update({n: p for n, p in app.providers.items() if s == "all" or p.access == s})
        elif s in app.providers:
            picked[s] = app.providers[s]
        else:
            raise ToolError(f"Unknown or disabled source '{s}'. Enabled: {sorted(app.providers)}")
    return list(picked.values())


@mcp.tool()
async def job_search(
    query: str,
    ctx: Context,
    sources: list[str] | None = None,
    limit_per_source: int = 25,
    include_known: bool = False,
) -> dict:
    """Search job sources and return de-duplicated postings.

    query: keywords, e.g. "unity xr" or "\"computer vision\" python". All words must match on feed sources.
    sources: names from job_sources, or "public" (default), "browser" (logged-in boards, slow, human-paced), "all".
    include_known: also return jobs already in Job_Search_Queue.csv / Job_Application_Tracker.csv.
    Each job carries is_new (first time this PC saw it) and known ("queue", "tracker", "archive") when applicable.
    Archive matches are still returned so a past rejection is visible.
    """
    app = _app(ctx)
    if not 1 <= limit_per_source <= 100:
        raise ToolError("limit_per_source must be 1-100")
    chosen = _pick(app, sources)
    try:
        known = load_known(app.cfg.queue_csv, app.cfg.tracker_csv, app.cfg.archive_tracker_csv)
    except CsvError as exc:
        raise ToolError(str(exc)) from exc

    errors, warnings, results = {}, [], []

    async def run(p: Provider):
        try:
            found = await p.search(query, limit_per_source)
            results.extend(found.jobs)
            warnings.extend(f"{p.name}: {w}" for w in found.warnings)
        except (ProviderError, BrowserError) as exc:
            errors[p.name] = str(exc)

    public = [p for p in chosen if p.access == "public"]
    await asyncio.gather(*(run(p) for p in public))
    for p in chosen:  # one browser window, so logged-in boards run one after another
        if p.access == "browser":
            await ctx.info(f"searching {p.name} in the browser")
            await run(p)

    jobs, seen_keys, counts = [], set(), {}
    for job in results:
        if job.key in seen_keys:
            continue
        seen_keys.add(job.key)
        where = known.lookup(job)
        if where in ("queue", "tracker") and not include_known:
            continue
        state = app.store.record(job)
        if state["mark"] == "skip" and not include_known:
            continue
        counts[job.source] = counts.get(job.source, 0) + 1
        jobs.append(_compact({**job.to_dict(), "extra": job.extra, "known": where, **state}))
    return _compact({"query": query, "count": len(jobs), "per_source": counts, "jobs": jobs,
                     "errors": errors, "warnings": warnings})


@mcp.tool()
async def job_details(url: str, ctx: Context, offset: int = 0, max_chars: int = 15000) -> dict:
    """Full posting text. Uses the board's API when one owns the URL, otherwise the logged-in browser."""
    app = _app(ctx)
    owner = next((p for p in app.providers.values() if p.access == "public" and p.owns_url(url)), None)
    try:
        if owner:
            text, via = await owner.details(url), owner.name
        else:
            await app.browser.open(url)
            page = await app.browser.read_text(offset, max_chars)
            return {"url": page["url"], "via": "browser", "title": page["title"],
                    "total_chars": page["total_chars"], "text": page["text"]}
    except (ProviderError, BrowserError) as exc:
        raise ToolError(str(exc)) from exc
    return {"url": url, "via": via, "total_chars": len(text), "text": text[offset:offset + max_chars]}


@mcp.tool()
async def job_mark(url: str, mark: str, ctx: Context, reason: str = "") -> str:
    """Remember a decision on a job this PC has seen: skip (hide from future searches), queued, or applied."""
    app = _app(ctx)
    try:
        updated = app.store.mark(normalize_url(url), mark, reason)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
    if not updated:
        raise ToolError("That URL has not come back from job_search on this PC yet")
    return f"marked {mark}"


@mcp.tool()
async def queue_add(
    company: str,
    position: str,
    url: str,
    source_board: str,
    ctx: Context,
    status: str = "New - evaluate",
    fit_score: str = "",
    category: str = "",
    remote_type: str = "",
    location_restriction: str = "",
    salary_range: str = "",
    notes: str = "",
    hire_odds: str = "",
    ghost_risk: str = "",
) -> str:
    """Append one row to Job_Search_Queue.csv (refuses duplicates). Evaluate with JOB_EVALUATION_GUIDE.md first."""
    app = _app(ctx)
    if not url.startswith("https://"):
        raise ToolError("url must be an https:// posting URL")
    job = Job(source=source_board, title=position, company=company, url=url)
    try:
        where = load_known(app.cfg.queue_csv, app.cfg.tracker_csv, app.cfg.archive_tracker_csv).lookup(job)
        if where in ("queue", "tracker"):
            raise ToolError(f"Already in the {where}")
        append_to_queue(app.cfg.queue_csv, {
            "Company": company, "Position": position, "URL": url, "Source Board": source_board, "Status": status,
            "Fit Score": fit_score, "Category": category, "Remote Type": remote_type,
            "Location Restriction": location_restriction, "Salary Range": salary_range, "Notes": notes,
            "Hire Odds": hire_odds, "Ghost Risk": ghost_risk,
        })
    except CsvError as exc:
        raise ToolError(str(exc)) from exc
    app.store.record(job)
    app.store.mark(job.key, "queued", "queue_add")
    return f"Queued {company} - {position}" + (" (note: matches an archived application)" if where == "archive" else "")


# ---------------------------------------------------------------- application browser


async def _browser_call(coro):
    try:
        return await coro
    except BrowserError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
async def browser_open(url: str, ctx: Context) -> dict:
    """Open a page (posting or application form) in the logged-in job-search Chrome window."""
    return await _browser_call(_app(ctx).browser.open(url))


@mcp.tool()
async def browser_read(ctx: Context, offset: int = 0, max_chars: int = 12000) -> dict:
    """Visible text of the current page, including embedded application iframes."""
    return await _browser_call(_app(ctx).browser.read_text(offset, max_chars))


@mcp.tool()
async def browser_form(ctx: Context, include_links: bool = False) -> dict:
    """List the current page's form fields and buttons with refs for browser_fill / choose / check / upload / click.

    Refs go stale after navigation or a step change; call this again then.
    """
    elements = await _browser_call(_app(ctx).browser.snapshot(include_links))
    return {"count": len(elements), "elements": [_compact(e) for e in elements]}


@mcp.tool()
async def browser_fill(ref: str, value: str, ctx: Context) -> str:
    """Type into a text field. Short values are typed key by key; long answers are pasted."""
    await _browser_call(_app(ctx).browser.fill(ref, value))
    return "filled"


@mcp.tool()
async def browser_choose(ref: str, option: str, ctx: Context) -> str:
    """Pick an option in a <select> or a type-to-filter dropdown, by its visible text."""
    return "chose " + await _browser_call(_app(ctx).browser.choose(ref, option))


@mcp.tool()
async def browser_check(ref: str, ctx: Context, checked: bool = True) -> str:
    """Tick or untick a checkbox / radio / switch."""
    await _browser_call(_app(ctx).browser.set_checked(ref, checked))
    return "checked" if checked else "unchecked"


@mcp.tool()
async def browser_upload(ref: str, file_path: str, ctx: Context) -> str:
    """Attach a file from the job's JobSearches/<Company>_<Role>/ folder (path relative to the repo root)."""
    return "uploaded " + await _browser_call(_app(ctx).browser.upload(ref, file_path))


@mcp.tool()
async def browser_click(ref: str, ctx: Context) -> dict:
    """Click a button or link: Apply, Next, Continue, Review, Upload. Final-submit buttons are refused by design."""
    return await _browser_call(_app(ctx).browser.click(ref))


@mcp.tool()
async def browser_press(ref: str, key: str, ctx: Context) -> dict:
    """Press Tab, Shift+Tab, ArrowDown, ArrowUp, Escape, Space, or Enter (Enter only on dropdowns) on an element."""
    return await _browser_call(_app(ctx).browser.press(ref, key))


@mcp.tool()
async def browser_screenshot(ctx: Context) -> Image:
    """Screenshot of the visible part of the current page, to check what was filled."""
    return Image(data=await _browser_call(_app(ctx).browser.screenshot()), format="png")


@mcp.tool()
async def browser_handoff(summary: str, ctx: Context) -> str:
    """Finish prep: bring the filled application to the front for the user to review and submit.

    summary: what was filled, which files were attached, and anything the user must answer or check.
    """
    url = await _browser_call(_app(ctx).browser.bring_to_front())
    log.info("handoff ready at %s", url.split("?")[0])
    return (f"Application left open for review at {url}. Tell the user: {summary}\n"
            "After the user submits, log it in Job_Application_Tracker.csv and job_mark(url, 'applied').")
