# Job Search Workflow

Use this when asked to actively find jobs the user may not have discovered yet.
This is different from evaluating a list the user already found - here Claude
searches job boards and surfaces new opportunities.

## Trigger Phrases

Start this workflow when user says any of:
- "check for jobs"
- "find new jobs"
- "job search"
- "look for positions"
- "scan job boards"

## Infrastructure Files

| File | Purpose |
|------|---------|
| `Job_Boards.csv` | Boards to search, category, region, last checked dates |
| `Job_Search_Queue.csv` | Jobs found, pending user review |
| `Job_Application_Tracker.csv` | All submitted applications |
| `job_mcp/` | Optional `job-search` MCP server that searches boards and fills applications (setup: `job_mcp/README.md`) |

**Job_Search_Queue.csv columns**: Company, Position, URL, Date Found, Source Board,
Status, Fit Score, Category, Remote Type, Location Restriction, Salary Range, Notes,
Hire Odds, Ghost Risk

**Row order = apply order**: sort by Hire Odds (A best .. D worst), then lowest Ghost Risk
(1-5). See `JOB_EVALUATION_GUIDE.md` @ Hire Odds and Ghost Risk.

**Status values**: New, Reviewing, Ready to Apply, Applied, Rejected, Saved for Later

Dates are ISO (`YYYY-MM-DD`) in every CSV.

## Phase 1 - Discovery

1. Read `Job_Boards.csv` for the board list and priorities
2. Check Last Checked dates - prioritize boards not searched recently
3. Search for postings matching the user's target keywords (`Search_Profile.md` @ Target Role Families,
   and the per-family search terms in `Job_Boards_Ranked.md`).
   - **With the `job-search` MCP**: `job_search(query)` searches the public feeds and company ATS
     boards by default; pass `sources=["browser"]` (or a board name such as `linkedin`) to page
     through logged-in boards at human pace, if the user enabled them. Results already in the queue
     or tracker are dropped; `known: "archive"` flags a past application. Read a posting with `job_details`.
   - **Without it**: WebSearch / WebFetch the boards' public search pages and company careers pages.
4. Apply automatic disqualifiers from `JOB_EVALUATION_GUIDE.md` - skip those immediately
5. Score each promising job using the scoring matrix in `JOB_EVALUATION_GUIDE.md`
6. Add to `Job_Search_Queue.csv` with Status: "New" and the fit score, Hire Odds and Ghost Risk
   (`queue_add` writes a correctly quoted row and refuses duplicates; `job_mark(url, "skip")` hides
   rejects from later searches)
7. Update Last Checked date in `Job_Boards.csv`

## Phase 2 - Review

1. Read `Job_Search_Queue.csv` for all Status: "New" entries
2. Present findings grouped by tier:

```
TIER 1 - Perfect Fit (Score 50+):
1. [Position] at [Company] - Score: XX | Hire Odds: X | Ghost Risk: X
   URL: [link]
   Key matches: [skills/domain]

TIER 2 - Strong Match (Score 35-49):
...

TIER 3 - Worth Considering (Score 20-34):
...
```

3. Ask which jobs to pursue
4. Update selected jobs to Status: "Reviewing"

## Phase 3 - Application Prep

For each job the user wants to pursue:
1. Fetch the full job description and save it to `JobSearches/<Company>_<Role>/JobDescription.txt`
   (create the folder if it doesn't exist)
2. If the job came from a job board, search for the company's own careers page and
   check if the same role is posted there directly - prefer the direct company URL
   for applying, note both links in the job description file
3. Follow the "Tailoring a resume" mode in `CLAUDE.md` (load order, precedence, Pre-Send Check)
4. For Tier 1/2 roles, draft outreach per `DIRECT_OUTREACH_WORKFLOW.md`
5. Update `Job_Search_Queue.csv` status to "Ready to Apply"
6. Notify user of: direct application URL (if found), resume location, cover letter location
7. **Optional, with the `job-search` MCP**: when the user says go, fill the application with the
   browser tools: `browser_open` the apply URL, `browser_form` to list fields, then `browser_fill` /
   `browser_choose` / `browser_check` / `browser_upload` (files must be in the job's `JobSearches/`
   folder). Every typed answer comes from the source of truth, the approved application responses
   file, or the job folder; a question with no documented answer is left blank and listed for the
   user. Finish with `browser_handoff`. The tools refuse the final Submit click and Enter in form
   fields; the user reviews and submits.

## Phase 4 - Post-Application

After user confirms application submitted:
1. Add entry to `Job_Application_Tracker.csv`:
   - Status: Applied
   - Follow-up Date: +1 week from submission
2. Update `Job_Search_Queue.csv` status to "Applied"
3. If the MCP is in use: `job_mark(url, "applied")`

When an application closes (rejected, ghosted after ~4 weeks, withdrawn), move its row to
`Archive/Job_Application_Tracker_Archive.csv` and its folder to `Archive/`. Keep real outcomes
(screens, interviews) visible; don't bulk-close rows.

## Board-Specific Notes

- **LinkedIn / FlexJobs / Arc.dev**: Only searchable through the `job-search` MCP's logged-in Chrome
  profile, and only if the user enabled them in `job_mcp/policy.yaml` (they ship disabled). Automated
  browsing is against these boards' terms and can get an account flagged; low page caps and human
  delays reduce but don't remove that risk.
- **Greenhouse / Lever / Ashby**: These are ATS platforms, not job boards. They have public JSON
  APIs per company (see `Job_Boards.csv` notes); add target companies to `job_mcp/policy.yaml`.
- **We Work Remotely / Remotive / Himalayas**: Good for remote-first companies. Check frequently.

## Limitations

Claude cannot:
- Type passwords or pass 2FA/CAPTCHA (the user signs in to each board by hand, once)
- Submit applications on the user's behalf (the browser tools refuse the final Submit)

User must:
- Sign in to logged-in boards in the job-search Chrome window when a session expires
- Review each filled application and click Submit
- Confirm when applications are sent so the tracker can be updated

## Quick Reference

| User Says | Claude Does |
|-----------|-------------|
| "check for jobs" | Phase 1 + 2 (Discovery + Review) |
| "prepare [Company] application" | Phase 3 for that job |
| "I applied to [Company]" | Phase 4 (update tracker) |
| "add job board [url]" | Add new row to Job_Boards.csv |
| "show queue" | Summarize Job_Search_Queue.csv |
| "show tracker" | Summarize Job_Application_Tracker.csv |
