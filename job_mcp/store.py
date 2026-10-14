"""Machine-local memory of jobs seen and skipped, so repeat searches surface only what is new."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .models import Job

_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    key TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    url TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    mark TEXT,
    mark_reason TEXT
)
"""
MARKS = ("skip", "queued", "applied")


class SeenStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(_SCHEMA)
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    def record(self, job: Job) -> dict:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._db.execute(
            "INSERT INTO jobs (key, source, title, company, url, first_seen, last_seen) VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(key) DO UPDATE SET last_seen = excluded.last_seen",
            (job.key, job.source, job.title, job.company, job.url, now, now),
        )
        self._db.commit()
        first_seen, mark = self._db.execute("SELECT first_seen, mark FROM jobs WHERE key = ?", (job.key,)).fetchone()
        return {"first_seen": first_seen, "is_new": first_seen == now, "mark": mark}

    def mark(self, key: str, mark: str, reason: str) -> bool:
        if mark not in MARKS:
            raise ValueError(f"mark must be one of {MARKS}")
        cur = self._db.execute("UPDATE jobs SET mark = ?, mark_reason = ? WHERE key = ?", (mark, reason, key))
        self._db.commit()
        return cur.rowcount == 1
