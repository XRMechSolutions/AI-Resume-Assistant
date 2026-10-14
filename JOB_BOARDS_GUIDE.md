# Job Boards Guide - Building and Maintaining Your Board List

How Claude works out which job boards are worth checking for this user, how often to check each,
and how to keep that list honest as results come in.

| File | Role |
|------|------|
| `Job_Boards.csv` | Machine-readable list Claude iterates during discovery: Board Name, URL, Category, Region, Tier, Vetting, Cost, Last Checked, Notes |
| `Job_Boards_Ranked.md` | Human-readable ranking: tiers, the user's account status per board, check frequency, search terms, results by board (start from `examples/Job_Boards_Ranked_Template.md`) |
| `Open_Calls.csv` | Target companies with no matching open role yet: talent pools, open applications, "check back" companies (start from `examples/Open_Calls_Template.csv`) |

## Step 1: First-Time Setup (run once, with the user)

1. Read `Search_Profile.md` (role families, location rules, pay floor, deal-breakers) and the
   Source of Truth's industries and Notes for Resume Customization.
2. Start from `Job_Boards.csv` (a broad, general-tech list) and the ranked template. For each board,
   decide **keep / drop**:
   - Drop boards whose region the user can't work in, and boards for fields they don't target
   - Keep every company-ATS source (Greenhouse, Lever, Ashby, Workable): they are direct to the employer
3. **Add niche boards** for the user's field. WebSearch "best job boards for [role family] [year]"
   and "[niche] jobs board remote", then verify each candidate is alive: it has postings dated within
   the last 30 days. Mark dead or absorbed boards as DEAD in Notes rather than deleting the row, so
   they don't get re-added later.
4. **Ask the user** which boards they already have accounts on, which vetted platforms
   (Arc.dev, Toptal, Turing...) they've applied to or been approved by, and which paid boards they
   pay for. Record it in the Your Status column. A vetted platform that has already placed the user
   is a warm channel; rank it above cold boards.
5. Write the search terms per role family into `Job_Boards_Ranked.md`. Use the titles employers post
   (check a few live postings), not the user's own title.
6. Build the target company list: companies in the user's niche that hire for their location. Add
   their ATS board tokens to `job_mcp/policy.yaml` (if the MCP is used) and any with no open role to
   `Open_Calls.csv`.

## Step 2: Check Frequency

Default cadence; adjust per board from the results table.

| Frequency | Boards |
|-----------|--------|
| **Daily** | The 1-2 highest-volume sources for the user's field, plus any vetted platform with active matches |
| **2-3x a week** | Company ATS boards for target companies (new postings get most of their applicants in the first 72 hours) |
| **Weekly** | Curated remote boards (We Work Remotely, Remotive, Remote OK, paid boards) |
| **Bi-weekly** | Specialized/niche boards, regional boards |
| **Monthly** | HN "Who is Hiring" (1st of the month), aggregator sweeps, vetted-platform profile refresh |
| **Per `Next Check`** | `Open_Calls.csv` rows |

During discovery, sort `Job_Boards.csv` by how overdue each board is (Last Checked + its cadence),
check the most overdue first, and update Last Checked after each board.

## Step 3: Learn From Results

Every few weeks (or when the user asks "which boards are working?"):

1. Count, per Source Board, rows in `Job_Search_Queue.csv` and `Job_Application_Tracker.csv`
   (including the archive tracker): queued, applied, and screens/interviews.
2. Update the Results by Board table in `Job_Boards_Ranked.md`.
3. Promote boards that produced screens (raise frequency); demote boards that produced only
   duplicates, stale postings, or ineligible-location roles (lower frequency or drop).
4. Note when a board mostly reposts jobs found elsewhere: check the original source instead.

## Open Calls (companies without a matching open role)

Some target companies have no fitting posting but run a talent pool, accept open applications, or
are worth rechecking. Track them in `Open_Calls.csv` instead of the queue:

- **Open Call Type**: Talent pool, Open application, No open role - recheck, Adjacent role open (ask about others)
- **Location Eligibility**: whether the user can work for them from where they live, and through what
  arrangement (remote employee, contractor, EOR)
- **Fit**: High / Medium / Low; order rows by eligibility, then fit
- **Next Check**: usually +30 days. When a matching role opens, move it to the queue and evaluate normally
- Submit to a talent pool only with a tailored resume; it's still an application

## Board Hygiene

- Prefer the company's own careers page over an aggregator listing of the same job
- Postings older than 60 days, reposted repeatedly, or worded as "future openings" get a high Ghost Risk
- Respect each board's terms: use official APIs/feeds where they exist; credit sources that require it
