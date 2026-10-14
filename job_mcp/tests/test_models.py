from job_mcp.models import normalize_url, title_key


def test_should_drop_tracking_params_when_normalizing():
    assert normalize_url("https://jobs.x.com/a/1/?utm_source=li&gh_jid=5") == "https://jobs.x.com/a/1?gh_jid=5"


def test_should_unify_linkedin_country_subdomains_when_normalizing():
    assert normalize_url("https://nl.linkedin.com/jobs/view/4472525663/") == \
        normalize_url("https://www.linkedin.com/jobs/view/4472525663")


def test_should_match_titles_when_punctuation_and_case_differ():
    assert title_key("GitLab", "Senior CX Platform Engineer") == title_key("gitlab ", "Senior CX-Platform engineer")
