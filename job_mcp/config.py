"""Loads policy.yaml and resolves machine-local paths."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = Path(__file__).resolve().parent / "policy.yaml"


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class BrowserPolicy:
    channel: str
    page_delay_s: tuple[float, float]
    action_delay_s: tuple[float, float]
    typing_delay_ms: tuple[int, int]
    max_snapshot_elements: int


@dataclass(frozen=True)
class SourcePolicy:
    name: str
    kind: str
    enabled: bool
    settings: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Config:
    repo_root: Path
    profile_dir: Path
    state_dir: Path
    log_path: Path
    user_agent: str
    http_min_delay_s: float
    browser: BrowserPolicy
    sources: dict[str, SourcePolicy]
    upload_roots: tuple[Path, ...]

    @property
    def queue_csv(self) -> Path:
        return self.repo_root / "Job_Search_Queue.csv"

    @property
    def tracker_csv(self) -> Path:
        return self.repo_root / "Job_Application_Tracker.csv"

    @property
    def archive_tracker_csv(self) -> Path:
        # Optional: closed applications moved out of the live tracker. Missing is fine.
        return self.repo_root / "Archive" / "Job_Application_Tracker_Archive.csv"


def _pair(raw, key: str, cast):
    if not isinstance(raw, list) or len(raw) != 2:
        raise ConfigError(f"policy.yaml: '{key}' must be a two-item list [min, max]")
    low, high = cast(raw[0]), cast(raw[1])
    if low < 0 or high < low:
        raise ConfigError(f"policy.yaml: '{key}' must satisfy 0 <= min <= max")
    return (low, high)


def _machine_state_dir() -> Path:
    # The browser profile holds live login sessions, so it lives outside the synced repo.
    override = os.environ.get("JOB_MCP_STATE_DIR")
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "job-mcp"
    return Path.home() / ".job-mcp"


def load_config(policy_path: Path = POLICY_PATH, repo_root: Path = REPO_ROOT) -> Config:
    try:
        raw = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"Cannot load {policy_path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"{policy_path} must be a mapping")

    try:
        http = raw["http"]
        b = raw["browser"]
        browser = BrowserPolicy(
            channel=str(b["channel"]),
            page_delay_s=_pair(b["page_delay_s"], "browser.page_delay_s", float),
            action_delay_s=_pair(b["action_delay_s"], "browser.action_delay_s", float),
            typing_delay_ms=_pair(b["typing_delay_ms"], "browser.typing_delay_ms", int),
            max_snapshot_elements=int(b["max_snapshot_elements"]),
        )
        sources = {
            name: SourcePolicy(
                name=name,
                kind=str(s["kind"]),
                enabled=bool(s["enabled"]),
                settings={k: v for k, v in s.items() if k not in ("kind", "enabled")},
            )
            for name, s in raw["sources"].items()
        }
        upload_roots = tuple((repo_root / p).resolve() for p in raw["upload_roots"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ConfigError(f"policy.yaml is missing or has a bad value: {exc}") from exc

    state_dir = _machine_state_dir()
    return Config(
        repo_root=repo_root,
        profile_dir=state_dir / "chrome-profile",
        state_dir=state_dir,
        log_path=state_dir / "job-mcp.log",
        user_agent=str(http["user_agent"]),
        http_min_delay_s=float(http["min_delay_s"]),
        browser=browser,
        sources=sources,
        upload_roots=upload_roots,
    )
