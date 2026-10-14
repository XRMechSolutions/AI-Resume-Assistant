import pytest

from job_mcp.browser.session import BrowserError, validate_upload_path
from job_mcp.config import ConfigError, load_config
from job_mcp.pacing import Pacer
from job_mcp.tests.fixtures.factories import run


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "JobSearches" / "Acme_XR").mkdir(parents=True)
    (tmp_path / "JobSearches" / "Acme_XR" / "resume.pdf").write_bytes(b"%PDF")
    (tmp_path / "Truth.md").write_text("private")
    (tmp_path / "Truth.pdf").write_bytes(b"%PDF")
    return tmp_path


def test_should_accept_upload_when_file_is_in_a_job_folder(repo):
    path = validate_upload_path("JobSearches/Acme_XR/resume.pdf", repo, (repo / "JobSearches",))
    assert path.name == "resume.pdf"


def test_should_refuse_upload_when_file_is_outside_upload_roots(repo):
    with pytest.raises(BrowserError):
        validate_upload_path("Truth.pdf", repo, (repo / "JobSearches",))


def test_should_refuse_upload_when_path_escapes_with_dotdot(repo):
    with pytest.raises(BrowserError):
        validate_upload_path("JobSearches/../Truth.pdf", repo, (repo / "JobSearches",))


def test_should_refuse_upload_when_extension_is_not_a_document(repo):
    with pytest.raises(BrowserError):
        validate_upload_path("Truth.md", repo, (repo,))


def test_should_load_repo_policy_when_state_dir_is_set(monkeypatch, tmp_path):
    monkeypatch.setenv("JOB_MCP_STATE_DIR", str(tmp_path))
    cfg = load_config()
    assert cfg.profile_dir == tmp_path / "chrome-profile"
    assert "linkedin" in cfg.sources and cfg.browser.page_delay_s[0] > 0


def test_should_fail_loudly_when_policy_has_bad_delay_pair(monkeypatch, tmp_path):
    monkeypatch.setenv("JOB_MCP_STATE_DIR", str(tmp_path))
    bad = tmp_path / "policy.yaml"
    bad.write_text("http: {user_agent: x, min_delay_s: 1}\nbrowser: {channel: chrome, page_delay_s: [5, 1], "
                   "action_delay_s: [1, 2], typing_delay_ms: [1, 2], max_snapshot_elements: 10}\n"
                   "upload_roots: [JobSearches]\nsources: {}\n")
    with pytest.raises(ConfigError):
        load_config(bad, tmp_path)


def test_should_space_calls_when_same_host_is_hit_twice():
    now, slept = [100.0], []

    async def fake_sleep(seconds):
        slept.append(seconds)
        now[0] += seconds

    pacer = Pacer(2.0, clock=lambda: now[0], sleep=fake_sleep)

    async def twice():
        await pacer.wait("a.com")
        await pacer.wait("a.com")
        await pacer.wait("b.com")

    run(twice())
    assert slept == [2.0]
