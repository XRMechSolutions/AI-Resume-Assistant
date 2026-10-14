"""One visible Chrome window on a dedicated, persistent profile, driven at human pace.

The profile keeps the board logins the person made by hand. Every action waits a random human-ish
delay first, and clicks or key presses that would send an application are refused (see guard.py).
"""

import asyncio
import logging
import random
import re
from pathlib import Path

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Frame, Page, async_playwright

from ..config import Config
from ..pacing import human_pause
from .guard import classify_click, classify_key

log = logging.getLogger("job_mcp.browser")

_SNAPSHOT_JS = (Path(__file__).parent / "snapshot.js").read_text(encoding="utf-8")
_REF = re.compile(r"^f(\d+)e\d+$")
_DESCRIBE_JS = """el => {
  const form = el.closest('form');
  return {
    tag: el.tagName.toLowerCase(), type: (el.getAttribute('type') || '').toLowerCase(),
    role: el.getAttribute('role') || '', text: (el.innerText || el.value || '').replace(/\\s+/g, ' ').trim().slice(0, 160),
    label: el.getAttribute('aria-label') || '', in_form: !!form,
    form_fields: form ? form.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea').length : 0,
    aria_autocomplete: el.getAttribute('aria-autocomplete') || '',
  };
}"""
_LINKS_JS = """({pattern, max}) => {
  const re = new RegExp(pattern);
  const seen = new Set();
  const out = [];
  for (const a of document.querySelectorAll('a[href]')) {
    if (out.length >= max) break;
    const m = a.href.match(re);
    if (!m || seen.has(m[0])) continue;
    seen.add(m[0]);
    const card = a.closest('li, article, [data-job-id], [data-jk], [class*="card" i], [class*="result" i]') || a;
    out.push({href: a.href, groups: [...m], text: (a.innerText || '').trim().slice(0, 200),
              card: (card.innerText || '').replace(/\\s+\\n/g, '\\n').trim().slice(0, 600)});
  }
  return out;
}"""
_TYPE_CHARS_LIMIT = 80  # longer answers are pasted, as a person would paste a prepared paragraph
_UPLOAD_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".rtf"}


class BrowserError(Exception):
    pass


def validate_upload_path(file_path: str, repo_root: Path, roots: tuple[Path, ...]) -> Path:
    path = Path(file_path)
    path = (path if path.is_absolute() else repo_root / path).resolve()
    if path.suffix.lower() not in _UPLOAD_EXTENSIONS:
        raise BrowserError(f"Uploads are limited to {sorted(_UPLOAD_EXTENSIONS)}")
    if not any(path.is_relative_to(root) for root in roots):
        raise BrowserError("Upload path must be inside the repo's allowed upload folders (policy.yaml upload_roots)")
    if not path.is_file():
        raise BrowserError(f"File not found: {path.name}")
    return path


class BrowserSession:
    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._policy = cfg.browser
        self._lock = asyncio.Lock()
        self._pw = None
        self._context = None
        self._page: Page | None = None
        self._frames: dict[str, Frame] = {}

    # ---------- lifecycle ----------

    async def _ensure_page(self) -> Page:
        if self._page and not self._page.is_closed():
            return self._page
        if self._context is None:
            self._cfg.profile_dir.mkdir(parents=True, exist_ok=True)
            if self._pw is None:  # survives the user closing the window; only the context is reopened
                self._pw = await async_playwright().start()
            try:
                self._context = await self._pw.chromium.launch_persistent_context(
                    str(self._cfg.profile_dir), channel=self._policy.channel, headless=False, no_viewport=True,
                    accept_downloads=False,
                )
            except PlaywrightError as exc:
                await self._pw.stop()
                self._pw = None
                raise BrowserError(f"Cannot start Chrome ({self._policy.channel}). Is the job-mcp profile already "
                                   f"open in another window? {exc}") from exc
            self._context.on("page", self._adopt_page)
            self._context.on("close", lambda _: self._reset())
            log.info("browser started with profile %s", self._cfg.profile_dir)
        pages = [p for p in self._context.pages if not p.is_closed()]
        self._page = pages[-1] if pages else await self._context.new_page()
        return self._page

    def _adopt_page(self, page: Page) -> None:
        # "Apply" buttons often open the ATS in a new tab; follow it like a person would.
        self._page = page
        self._frames.clear()

    def _reset(self) -> None:
        self._context, self._page = None, None
        self._frames.clear()

    async def wait_until_closed(self) -> None:
        """Blocks until the person closes the Chrome window (used by the login command)."""
        if self._context is None:
            return
        closed = asyncio.Event()
        self._context.on("close", lambda _: closed.set())
        await closed.wait()

    async def close(self) -> None:
        if self._context:
            await self._context.close()
        if self._pw:
            await self._pw.stop()
        self._reset()
        self._pw = None

    # ---------- navigation and reading ----------

    async def open(self, url: str) -> dict:
        if not re.match(r"^https://", url):
            raise BrowserError("Only https:// URLs are opened")
        async with self._lock:
            page = await self._ensure_page()
            await human_pause(self._policy.page_delay_s)
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            except PlaywrightError as exc:
                raise BrowserError(f"Navigation failed: {exc}") from exc
            self._frames.clear()
            await self._settle(page)
            log.info("opened %s", page.url.split("?")[0])
            return {"url": page.url, "title": await page.title()}

    async def _settle(self, page: Page) -> None:
        try:
            await page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightError:
            pass  # long-polling pages never go idle; the DOM is already loaded

    async def scroll_through(self, steps: int = 4) -> None:
        async with self._lock:
            page = await self._ensure_page()
            for _ in range(steps):
                await page.mouse.wheel(0, random.randint(500, 1100))
                await human_pause(self._policy.action_delay_s)

    async def read_text(self, offset: int, max_chars: int) -> dict:
        async with self._lock:
            page = await self._ensure_page()
            chunks = []
            for frame in page.frames:
                try:
                    text = await frame.evaluate("() => document.body ? document.body.innerText : ''")
                except PlaywrightError:
                    continue
                if text.strip() and (frame is page.main_frame or len(text) > 200):
                    chunks.append(text if frame is page.main_frame else f"\n\n[frame {frame.url[:80]}]\n{text}")
            full = re.sub(r"\n{3,}", "\n\n", "".join(chunks))
            return {"url": page.url, "title": await page.title(), "total_chars": len(full),
                    "offset": offset, "text": full[offset:offset + max_chars]}

    async def links_matching(self, pattern: str, max_links: int) -> dict:
        async with self._lock:
            page = await self._ensure_page()
            links = await page.evaluate(_LINKS_JS, {"pattern": pattern, "max": max_links})
            sample = [] if links else await page.evaluate(
                "() => [...document.querySelectorAll('a[href]')].slice(0, 400).map(a => a.href)"
                ".filter((h, i, a) => a.indexOf(h) === i).slice(0, 25)")
            return {"url": page.url, "title": await page.title(), "links": links, "sample_hrefs": sample}

    async def cookie_names(self, domain: str) -> list[str]:
        async with self._lock:
            await self._ensure_page()
            return [c["name"] for c in await self._context.cookies() if c["domain"].lstrip(".").endswith(domain)]

    async def screenshot(self) -> bytes:
        async with self._lock:
            page = await self._ensure_page()
            return await page.screenshot(full_page=False, type="png")

    async def bring_to_front(self) -> str:
        async with self._lock:
            page = await self._ensure_page()
            await page.bring_to_front()
            return page.url

    # ---------- forms ----------

    async def snapshot(self, include_links: bool) -> list[dict]:
        async with self._lock:
            page = await self._ensure_page()
            self._frames.clear()
            elements: list[dict] = []
            budget = self._policy.max_snapshot_elements
            for i, frame in enumerate(page.frames):
                if len(elements) >= budget:
                    break
                prefix = f"f{i}e"
                try:
                    found = await frame.evaluate(_SNAPSHOT_JS, {"prefix": prefix, "max": budget - len(elements),
                                                                "includeLinks": include_links})
                except PlaywrightError:
                    continue  # cross-origin frames that are mid-navigation
                if found:
                    self._frames[prefix] = frame
                    if frame is not page.main_frame:
                        for el in found:
                            el["frame"] = frame.url[:100]
                    elements.extend(found)
            return elements

    def _locate(self, ref: str):
        m = _REF.match(ref)
        frame = self._frames.get(f"f{m.group(1)}e") if m else None
        if frame is None or frame.is_detached():
            raise BrowserError(f"Unknown or stale ref '{ref}'; call browser_form again")
        return frame, frame.locator(f'[data-jm-ref="{ref}"]')

    async def _describe(self, locator) -> dict:
        if await locator.count() != 1:
            raise BrowserError("Element is gone; call browser_form again")
        return await locator.evaluate(_DESCRIBE_JS)

    async def fill(self, ref: str, value: str) -> None:
        async with self._lock:
            _, loc = self._locate(ref)
            await self._describe(loc)
            await human_pause(self._policy.action_delay_s)
            await loc.scroll_into_view_if_needed()
            await loc.click()
            await loc.fill("")
            if len(value) <= _TYPE_CHARS_LIMIT:
                await loc.press_sequentially(value, delay=random.randint(*self._policy.typing_delay_ms))
            else:
                await loc.fill(value)

    async def choose(self, ref: str, option: str) -> str:
        async with self._lock:
            frame, loc = self._locate(ref)
            desc = await self._describe(loc)
            await human_pause(self._policy.action_delay_s)
            await loc.scroll_into_view_if_needed()
            if desc["tag"] == "select":
                try:
                    picked = await loc.select_option(label=option)
                except PlaywrightError:
                    picked = await loc.select_option(value=option)
                return ", ".join(picked)
            # Custom dropdowns (React-Select and similar): open, type to filter, click the match.
            await loc.click()
            await loc.press_sequentially(option, delay=random.randint(*self._policy.typing_delay_ms))
            await human_pause(self._policy.action_delay_s)
            match = frame.get_by_role("option", name=re.compile(re.escape(option), re.I)).first
            try:
                await match.click(timeout=5_000)
            except PlaywrightError as exc:
                raise BrowserError(f"No dropdown option matching '{option}' appeared") from exc
            return option

    async def set_checked(self, ref: str, checked: bool) -> None:
        async with self._lock:
            _, loc = self._locate(ref)
            await self._describe(loc)
            await human_pause(self._policy.action_delay_s)
            await loc.scroll_into_view_if_needed()
            await loc.set_checked(checked)

    async def upload(self, ref: str, file_path: str) -> str:
        path = validate_upload_path(file_path, self._cfg.repo_root, self._cfg.upload_roots)
        async with self._lock:
            page = await self._ensure_page()
            _, loc = self._locate(ref)
            desc = await self._describe(loc)
            await human_pause(self._policy.action_delay_s)
            if desc["type"] == "file":
                await loc.set_input_files(str(path))
            else:
                async with page.expect_file_chooser(timeout=10_000) as chooser:
                    await loc.click()
                await (await chooser.value).set_files(str(path))
            log.info("uploaded %s", path.name)
            return path.name

    async def click(self, ref: str) -> dict:
        async with self._lock:
            page = await self._ensure_page()
            _, loc = self._locate(ref)
            verdict = classify_click(await self._describe(loc))
            if not verdict.allowed:
                log.info("blocked click on %s: %s", ref, verdict.reason)
                return {"clicked": False, "blocked": verdict.reason}
            await human_pause(self._policy.action_delay_s)
            await loc.scroll_into_view_if_needed()
            await loc.click()
            await self._settle(self._page or page)
            self._frames.clear()
            current = self._page or page
            return {"clicked": True, "url": current.url, "title": await current.title()}

    async def press(self, ref: str, key: str) -> dict:
        async with self._lock:
            _, loc = self._locate(ref)
            verdict = classify_key(key, await self._describe(loc))
            if not verdict.allowed:
                return {"pressed": False, "blocked": verdict.reason}
            await human_pause(self._policy.action_delay_s)
            await loc.press(key)
            return {"pressed": True}
