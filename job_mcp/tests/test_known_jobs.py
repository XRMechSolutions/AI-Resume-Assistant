import csv

import pytest

from job_mcp.known_jobs import QUEUE_COLUMNS, CsvError, append_to_queue, load_known
from job_mcp.tests.fixtures.factories import make_job

TRACKER_COLUMNS = ["Company", "Position", "Date Applied", "Status"]


@pytest.fixture
def csvs(tmp_path):
    queue = tmp_path / "queue.csv"
    tracker = tmp_path / "tracker.csv"
    with queue.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        w.writerow(QUEUE_COLUMNS)
        w.writerow(["Acme XR", "Senior Unity Developer", "https://nl.linkedin.com/jobs/view/111/"] + [""] * 11)
    with tracker.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL)
        w.writerow(TRACKER_COLUMNS)
        w.writerow(["Acme Labs", "App Developer", "2024-12-30", "Contract"])
    return queue, tracker, tmp_path / "missing-archive.csv"


def test_should_find_queued_job_when_url_differs_only_by_subdomain(csvs):
    known = load_known(*csvs)
    assert known.lookup(make_job(url="https://www.linkedin.com/jobs/view/111", company="x", title="y")) == "queue"


def test_should_find_tracked_job_when_matching_by_company_and_title(csvs):
    known = load_known(*csvs)
    assert known.lookup(make_job(company="Acme Labs", title="App Developer")) == "tracker"


def test_should_return_none_when_job_is_unknown(csvs):
    assert load_known(*csvs).lookup(make_job(company="Unseen Co", title="Robotics Engineer")) is None


def test_should_raise_when_queue_csv_is_missing(csvs, tmp_path):
    with pytest.raises(CsvError):
        load_known(tmp_path / "nope.csv", csvs[1], csvs[2])


def test_should_append_quoted_row_with_date_when_adding_to_queue(csvs):
    queue = csvs[0]
    append_to_queue(queue, {"Company": "Beta", "Position": "AR Engineer", "URL": "https://b.io/j/1", "Notes": 'a, "b"'})
    with queue.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[-1]["Company"] == "Beta" and rows[-1]["Notes"] == 'a, "b"' and rows[-1]["Date Found"]
    assert len(rows) == 2


def test_should_refuse_unknown_column_when_adding_to_queue(csvs):
    with pytest.raises(CsvError):
        append_to_queue(csvs[0], {"Salary": "1"})
