# job-search MCP server (optional)

A local MCP server for Claude Code that finds postings across job boards and walks an application
up to, **never through**, the final Submit. It serves `JOB_SEARCH_WORKFLOW.md` Phases 1 and 3.
Everything else in this repo works without it.

## Setup (once per PC)

From the repo root (Windows paths shown; use `.venv/bin/python` on macOS/Linux):

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
claude mcp add --scope local --env PYTHONPATH=<repo root> --transport stdio job-search -- <repo root>/.venv/Scripts/python.exe -m job_mcp
.\.venv\Scripts\python.exe -m job_mcp check
```

`check` loads `policy.yaml` and lists the enabled sources without touching the network. It needs
`Job_Search_Queue.csv` and `Job_Application_Tracker.csv` at the repo root (copy them from `examples/`).
The browser tools use your installed Google Chrome (`channel: chrome` in `policy.yaml`).

Then edit `policy.yaml`:
- **Company ATS boards**: put the companies you target under `greenhouse` / `lever` / `ashby`
  (the token from their careers URL, e.g. `jobs.ashbyhq.com/<token>`)
- **Logged-in boards** (LinkedIn, FlexJobs, Arc.dev, Indeed) ship **disabled**. Automated browsing is
  against those boards' terms and can get your account flagged. Enable one only if you accept that
  risk, then in a Claude session run `job_login("linkedin")` and sign in by hand in the Chrome window.

## Tools

Discovery: `job_sources`, `job_login`, `job_search`, `job_details`, `job_mark`, `queue_add`.
Applying: `browser_open`, `browser_read`, `browser_form`, `browser_fill`, `browser_choose`,
`browser_check`, `browser_upload`, `browser_click`, `browser_press`, `browser_screenshot`, `browser_handoff`.

## Safety guarantees

- **No final submit.** Submit-worded buttons ("Submit application", "Review and submit") and any
  unlabeled/"Apply" submit button on a form with 3+ fields are refused, as is Enter in form fields.
  "Apply"/"Easy Apply" openers and Next/Continue/Review steps are allowed. You review and submit.
- **Uploads only from `JobSearches/`** (`upload_roots`), document extensions only, `..` resolved
  first. Your source of truth and voice files can never be attached.
- **Logins never touch the repo.** The Chrome profile lives in `%LOCALAPPDATA%\job-mcp\chrome-profile`
  (`~/.job-mcp` elsewhere; override with `JOB_MCP_STATE_DIR`). No passwords are stored or typed.
- **Human pace.** Browser: 6-15 s before each page, 1.2-3.5 s before each action, per-key typing for
  short answers. Public APIs: 1.5 s minimum per host; whole-feed sources cached 30 min.
- **Errors are loud.** A failing source is reported in `errors`; misconfigured sources show in
  `job_sources.not_loaded`.

Seen/skipped jobs are remembered per PC in `seen.sqlite` and the log is `job-mcp.log`, both in the
state folder above.

## Tests

```
.\.venv\Scripts\python.exe -m pytest job_mcp/tests -q
```
Unit tests only (no network, no browser).

## Gotchas

- Greenhouse double-escapes `content`; `html_to_text` unescapes once.
- Remotive's `search` is fuzzy; results are filtered locally.
- Remote OK terms: credit Remote OK and keep its URL. Remotive terms: never republish its jobs.
- Greenhouse file inputs are hidden behind "Attach" buttons; `browser_form` reports `id` (`resume`,
  `cover_letter`) and `group` ("Resume/CV*", "Cover Letter") to tell them apart.
- React-Select dropdowns appear twice (a combobox with the question label, plus a hidden required
  "Select..." input). Use the combobox with `browser_choose`.
- Only one process can open the Chrome profile. Close the `login` CLI window before the MCP server uses it.
- Restart the MCP server after editing `policy.yaml`.
