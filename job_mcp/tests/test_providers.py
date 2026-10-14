import pytest

from job_mcp.providers.ats import Ashby, Greenhouse
from job_mcp.providers.base import ProviderError, html_to_text, matches_query
from job_mcp.providers.feeds import HackerNewsHiring, RemoteOK, WeWorkRemotely
from job_mcp.tests.fixtures.factories import make_http, run

GH = "https://boards-api.greenhouse.io/v1/boards/"


def _gh_job(job_id: int, title: str) -> dict:
    return {"id": job_id, "title": title, "company_name": "GitLab", "location": {"name": "Remote"},
            "absolute_url": f"https://job-boards.greenhouse.io/gitlab/jobs/{job_id}", "departments": [],
            "first_published": "2026-10-01T00:00:00Z"}


def test_should_filter_greenhouse_titles_when_searching():
    http = make_http({GH + "gitlab/jobs": {"jobs": [_gh_job(1, "Unity Engineer"), _gh_job(2, "Account Executive")]}})
    found = run(Greenhouse("greenhouse", http, ["gitlab"]).search("unity", 10))
    assert [j.title for j in found.jobs] == ["Unity Engineer"]


def test_should_warn_but_return_jobs_when_one_company_board_fails():
    http = make_http({GH + "gitlab/jobs": {"jobs": [_gh_job(1, "Unity Engineer")]}, GH + "gone/jobs": 404})
    found = run(Greenhouse("greenhouse", http, ["gitlab", "gone"]).search("", 10))
    assert len(found.jobs) == 1 and found.warnings


def test_should_raise_when_every_company_board_fails():
    http = make_http({GH: 500})
    with pytest.raises(ProviderError):
        run(Greenhouse("greenhouse", http, ["gitlab"]).search("", 10))


def test_should_raise_when_greenhouse_is_enabled_without_companies():
    with pytest.raises(ProviderError):
        Greenhouse("greenhouse", make_http({}), [])


def test_should_unescape_greenhouse_content_when_fetching_details():
    http = make_http({GH + "gitlab/jobs/7": {"content": "&lt;p&gt;Build &amp;amp; ship&lt;/p&gt;&lt;ul&gt;&lt;li&gt;Unity&lt;/li&gt;&lt;/ul&gt;"}})
    text = run(Greenhouse("greenhouse", http, ["gitlab"]).details("https://job-boards.greenhouse.io/gitlab/jobs/7"))
    assert "Build & ship" in text and "- Unity" in text


def test_should_raise_when_ashby_no_longer_lists_the_job():
    http = make_http({"https://api.ashbyhq.com/posting-api/job-board/alan": {"jobs": []}})
    url = "https://jobs.ashbyhq.com/alan/583a9a1c-433e-4b76-a1b7-4d9e6a30f1da"
    with pytest.raises(ProviderError):
        run(Ashby("ashby", http, ["alan"]).details(url))


def test_should_skip_legal_notice_when_reading_remoteok():
    feed = [{"legal": "terms"}, {"position": "Python Engineer", "company": "Z", "url": "https://remoteok.com/r/1",
                                 "tags": ["python"], "salary_min": 100000, "salary_max": 150000}]
    found = run(RemoteOK(make_http({"https://remoteok.com/api": feed})).search("python", 10))
    assert found.jobs[0].salary == "$100,000-$150,000"


def test_should_split_company_from_title_when_reading_wwr_rss():
    rss = ("<rss><channel><item><title>Acme: Backend Engineer</title><link>https://weworkremotely.com/r/1</link>"
           "<region>Anywhere</region></item></channel></rss>")
    found = run(WeWorkRemotely(make_http({"https://weworkremotely.com/": rss}), ["remote-programming-jobs"]).search("", 5))
    assert (found.jobs[0].company, found.jobs[0].title) == ("Acme", "Backend Engineer")


def test_should_keep_only_top_level_comments_when_reading_hn_hiring():
    stories = {"hits": [{"objectID": "900", "title": "Ask HN: Who is hiring? (October 2026)"}]}
    comments = {"hits": [
        {"objectID": "1", "parent_id": 900, "comment_text": "Acme | XR Engineer | Remote (EU)<p>Unity", "created_at": "x"},
        {"objectID": "2", "parent_id": 1, "comment_text": "Is this still open?", "created_at": "x"},
    ]}
    http = make_http({"https://hn.algolia.com/api/v1/search_by_date": stories, "https://hn.algolia.com/api/v1/search": comments})
    found = run(HackerNewsHiring(http).search("unity", 10))
    assert [(j.company, j.title) for j in found.jobs] == [("Acme", "XR Engineer")]


def test_should_require_every_term_when_matching_query():
    assert matches_query('unity "computer vision"', "Unity Computer Vision Engineer")
    assert not matches_query("unity rust", "Unity Engineer")


def test_should_drop_scripts_when_converting_html():
    assert html_to_text("<p>Hi</p><script>evil()</script>") == "Hi"
