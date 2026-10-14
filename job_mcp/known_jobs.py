"""Reads and appends the repo's job CSVs so search results skip what is already queued or applied."""

import csv
import io
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .models import Job, normalize_url, title_key

QUEUE_COLUMNS = [
    "Company", "Position", "URL", "Date Found", "Source Board", "Status", "Fit Score", "Category",
    "Remote Type", "Location Restriction", "Salary Range", "Notes", "Hire Odds", "Ghost Risk",
]


class CsvError(Exception):
    pass


@dataclass(frozen=True)
class KnownIndex:
    by_url: dict[str, str]
    by_title: dict[str, str]

    def lookup(self, job: Job) -> str | None:
        return self.by_url.get(job.key) or self.by_title.get(title_key(job.company, job.title))


def _rows(path: Path) -> list[dict]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))
    except OSError as exc:
        raise CsvError(f"Cannot read {path.name}: {exc}") from exc


def load_known(queue: Path, tracker: Path, archive: Path) -> KnownIndex:
    """Later sources never overwrite earlier ones, so a live queue/tracker row wins over the archive."""
    by_url: dict[str, str] = {}
    by_title: dict[str, str] = {}
    for label, path, url_col in (("queue", queue, "URL"), ("tracker", tracker, None), ("archive", archive, None)):
        if not path.exists():
            if label == "archive":
                continue
            raise CsvError(f"{path.name} is missing")
        for row in _rows(path):
            company, position = row.get("Company", ""), row.get("Position", "")
            if company and position:
                by_title.setdefault(title_key(company, position), label)
            url = (row.get(url_col) if url_col else row.get("Job URL")) or ""
            if url.startswith("http"):
                by_url.setdefault(normalize_url(url), label)
    return KnownIndex(by_url, by_title)


def append_to_queue(queue: Path, values: dict[str, str]) -> None:
    unknown = set(values) - set(QUEUE_COLUMNS)
    if unknown:
        raise CsvError(f"Unknown queue columns: {sorted(unknown)}")
    with queue.open(encoding="utf-8-sig", newline="") as fh:
        header = next(csv.reader(fh), None)
    if header != QUEUE_COLUMNS:
        raise CsvError("Job_Search_Queue.csv header changed; update QUEUE_COLUMNS in known_jobs.py first")
    row = {c: "" for c in QUEUE_COLUMNS}
    row["Date Found"] = date.today().isoformat()
    row.update(values)
    buf = io.StringIO()
    csv.DictWriter(buf, fieldnames=QUEUE_COLUMNS, quoting=csv.QUOTE_ALL, lineterminator="\r\n").writerow(row)
    raw = queue.read_bytes()
    with queue.open("a", encoding="utf-8", newline="") as fh:
        if raw and not raw.endswith(b"\n"):
            fh.write("\r\n")
        fh.write(buf.getvalue())
