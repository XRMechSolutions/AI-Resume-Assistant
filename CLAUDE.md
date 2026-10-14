# CLAUDE.md - AI Resume Assistant

This file guides every AI agent working in this job-search repository: Claude Code reads it directly,
and Codex / Gemini CLI reach it through the `AGENTS.md` / `GEMINI.md` pointers. It applies to an agent
started anywhere in the repo, including inside a `JobSearches/<Company>_<Role>/` folder. "Claude"
below means whichever agent is reading.

This is a **document project**: a source-of-truth experience record, tailored resumes (.txt -> PDF),
cover letters, outreach, application tracking and interview prep. Workflow detail lives in the root
`*.md` guides; this file says which to load for each kind of work, and what "done" means. This file is
shared and has no personal content: the user's settings live in `Search_Profile.md` and their facts in
`Source_of_Truth.md` (both git-ignored).

---

## Step 0: Setup Check (every session, before anything else)

Check that `Search_Profile.md` and `Source_of_Truth.md` exist at the repo root and that
`Search_Profile.md` says `Setup status: **complete**`.

If either file is missing, or setup is incomplete: **stop and run `SETUP.md` with the user**,
resuming at the first unchecked step. Do not write resumes, cover letters, outreach or applications
until setup is complete. Evaluating a posting the user pastes is fine, but say the result is
provisional until setup is done.

---

## Hard Rules (every task)

1. **Never invent experience.** Every claim in outgoing material must trace to
   `Source_of_Truth.md`. Not found -> don't add it. Unsure -> ask the user.
   Unconfirmed facts are parked in `Unconfirmed_Facts.md` - never use anything in its Open table.
2. **Confidentiality.** Respect NDAs and client confidentiality, per `Search_Profile.md` @
   Confidentiality Rules.
3. **Edit the source, then derive.** Change a fact in the source of truth first, then the base resumes,
   then tailored resumes and letters. Never fix a fact only in a derived file.
4. **The user's voice.** Outgoing text sounds like the user (`VoiceMatching/Voice_Profile.md`),
   never generic AI prose. Recruiters reject generic AI text; tailoring is the point.
5. **The user submits.** Claude prepares applications; the user reviews and sends every application,
   email and message.

### GOLDEN RULE
**If it's not in the source documents, DO NOT add it to the resume.**
- No similar technologies (e.g., Vue.js when they know React)
- No made-up metrics (performance improvements, cost savings)
- No assumed experience (e.g., Unreal because they know Unity)

For each job requirement: search the source documents -> found: use exact wording -> not found: DO
NOT ADD -> uncertain: ASK the user (and log it in `Unconfirmed_Facts.md`).

---

## Mode Routing - load these, in order, before substantive work

Load only what the current task needs. When the task changes mode, load that mode's files.

| Mode (you are...) | Load | Output goes to |
|---|---|---|
| Updating the user's experience / profile | ANTI_FABRICATION_CHECKLIST.md; Source of Truth (edit target) | Source of Truth -> affected base resumes |
| Evaluating a job posting | JOB_EVALUATION_GUIDE.md; Search_Profile.md; Source of Truth @ DO NOT CLAIM; Job_Application_Tracker.csv (duplicate check) | Verdict + tier in chat; queue row if pursuing; unmet requirements -> Showpiece_Backlog.md Gap Log |
| Finding jobs / working out which boards to check | JOB_SEARCH_WORKFLOW.md; JOB_BOARDS_GUIDE.md; Search_Profile.md @ Target Role Families; Job_Boards.csv; Job_Boards_Ranked.md | Job_Search_Queue.csv; Open_Calls.csv; Last Checked dates |
| Tailoring a resume | ANTI_FABRICATION_CHECKLIST.md; Source of Truth; Unconfirmed_Facts.md; RESUME_TXT_FORMAT.md; RESUME_CRAFTING_GUIDELINES.md; nearest base resume | `JobSearches/<Company>_<Role>/` (.txt + PDF, .docx if needed) + Prep_Notes.md |
| Writing a cover letter / application answers | Voice Profile; Application_Responses.md (incl. Disclosure Risk Notes); Source of Truth; ANTI_FABRICATION_CHECKLIST.md | Company folder; `create_cover_letter_docx.py` for .docx |
| Outreach to a hiring manager / referral | DIRECT_OUTREACH_WORKFLOW.md; Voice Profile; Project_Demo_Videos.md | Company folder + tracker Outreach columns |
| Filling an application with the job-search MCP | job_mcp/README.md; JOB_SEARCH_WORKFLOW.md Phase 3; plus the Writing-answers loads above | Filled form handed off with `browser_handoff` |
| Logging / following up an application | Tracker conventions below | Job_Application_Tracker.csv |
| Setting up, or changing the user's targets / criteria | SETUP.md; Search_Profile.md | Search_Profile.md (+ Decisions Log) |
| Interview prep | Source of Truth; Application_Responses.md; company folder notes; examples/Interview_Notes_Template.md | `JobSearches/<Company>_<Role>/Interview_Notes.md` |
| Portfolio / personal brand | PORTFOLIO_READINESS.md; Project_Demo_Videos.md | Those files |
| Suggesting / tracking demo projects for job gaps | SHOWPIECE_WORKFLOW.md; Showpiece_Backlog.md | Showpiece_Backlog.md |
| Building or recalibrating the voice profile | VoiceMatching/README.md | VoiceMatching/Voice_Profile.md |

## Precedence When Standards Conflict

Highest wins:
1. **ANTI_FABRICATION_CHECKLIST + Source of Truth "DO NOT CLAIM"** - beat everything
2. **Confidentiality rules** (Hard Rule 2)
3. **RESUME_TXT_FORMAT.md** (the PDF parser contract) beats any formatting advice elsewhere.
   One bullet = one line; `•` bullets (a `- ` item only under a `Heading:` sub-section)
4. **Voice Profile banned words and phrases** beat word suggestions in the crafting guidelines
5. **RESUME_CRAFTING_GUIDELINES.md** for tone and structure

## Pre-Send Check (what "done" means for any outgoing material)

- [ ] Every claim found in the Source of Truth; nothing from Unconfirmed Facts (Open); nothing from DO NOT CLAIM
- [ ] Confidentiality-safe (Hard Rule 2)
- [ ] .txt rules: exact section headers, one-line bullets, no `&`, location line 3 words or fewer
- [ ] `python create_pdf.py "<file>.txt" "<out>.pdf"` succeeds with no `[WARN]` lines (it reports the page count and warns above 2 pages)
- [ ] No AI-marker words (RESUME_CRAFTING_GUIDELINES §1) or Voice Profile banned phrases
- [ ] Contact header matches `Search_Profile.md`; dates match the Source of Truth; titles are real titles

Record the result at the bottom of the job's `Prep_Notes.md`.

---

## Repository Structure

| Path | What |
|---|---|
| `Source_of_Truth.md` | Master fact record - the only authority for claims (DO NOT CLAIM list included) |
| `Search_Profile.md` | The user's settings: contact header, target roles + base resumes, location, pay, deal-breakers, confidentiality, decisions log, setup status |
| `SETUP.md` / `Questionnaire_Answers.md` | Agent-run onboarding / the user's raw answers |
| `Unconfirmed_Facts.md` | Facts awaiting confirmation or disclosure approval |
| `ANTI_FABRICATION_CHECKLIST.md` | Claim-verification standard |
| `RESUME_CRAFTING_GUIDELINES.md` / `RESUME_TXT_FORMAT.md` | Tone/structure standard / .txt parser contract |
| `<Name>Resume_<Variant>.txt/.pdf` | Base resumes, one per role family |
| `create_pdf.py` / `create_cover_letter_docx.py` | .txt -> PDF (+ `--docx`) / cover letter .docx |
| `Application_Responses.md` | Approved answers + disclosure risk notes |
| `VoiceMatching/` | Voice profile and the raw writing it was built from |
| `JOB_EVALUATION_GUIDE.md`, `JOB_SEARCH_WORKFLOW.md`, `JOB_BOARDS_GUIDE.md`, `DIRECT_OUTREACH_WORKFLOW.md`, `SHOWPIECE_WORKFLOW.md` | Workflow guides |
| `Job_Boards.csv`, `Job_Boards_Ranked.md`, `Open_Calls.csv` | Where to look, how often, and target companies with no open role |
| `Job_Search_Queue.csv`, `Job_Application_Tracker.csv` | Found jobs pending review (rows in apply order) / applications |
| `Showpiece_Backlog.md`, `PORTFOLIO_READINESS.md`, `Project_Demo_Videos.md` | Gap log + demo ideas, portfolio checklist, public demo links |
| `JobSearches/<Company>_<Role>/` | Per-application folder: Job_Description.md, tailored resume, cover letter, Prep_Notes.md, Interview_Notes.md |
| `Archive/` | Closed applications (folders + `Job_Application_Tracker_Archive.csv`); reference only |
| `job_mcp/` | Optional job-search MCP server |

## How the Pieces Fit (workstreams)

| Workstream | Layer | Owns | Contract |
|---|---|---|---|
| profile | 0 | Source of Truth, Unconfirmed_Facts, Voice Profile, PORTFOLIO_READINESS, Project_Demo_Videos | The Source of Truth is the only authority for claims |
| resumes | 1 | ANTI_FABRICATION_CHECKLIST, crafting guidelines, .txt format, base resumes, create_pdf.py | A .txt that passes the Pre-Send Check and renders to 2 pages or less |
| applications | 1 | Workflow guides, Application_Responses, trackers, board files, cover letter script, `JobSearches/` | One tracker row + one `JobSearches/<Company>_<Role>/` folder per application |
| job-mcp (optional) | 1 | `job_mcp/` | Never clicks a final Submit; uploads only from `JobSearches/`; logins live outside the repo |
| interviews | 2 | `JobSearches/*/Interview_Notes.md`, story bank | Stories only from the Source of Truth |
| showpieces | 2 | SHOWPIECE_WORKFLOW, Showpiece_Backlog | Every evaluated posting's gaps land in the Gap Log; a showpiece counts as experience only once it's done and in the Source of Truth |

Layer 0 is the source of facts; Layer 1 derives from it; Layer 2 draws on both. A fact flows
profile -> resumes/applications -> interviews, never backwards: if you find an error in a derived
file, fix it in the Source of Truth first (Hard Rule 3).

## Where to Pick Up

| I want to... | Go to... |
|---|---|
| See what's waiting to be applied for | `Job_Search_Queue.csv` (rows in apply order) |
| See live applications and follow-ups due | `Job_Application_Tracker.csv` |
| See where a specific application stands | `JobSearches/<Company>_<Role>/Prep_Notes.md` |
| See unconfirmed facts | `Unconfirmed_Facts.md` |
| See recurring skill gaps | `Showpiece_Backlog.md` Gap Log |
| See the user's targets and decisions already made | `Search_Profile.md` (Decisions Log) |

## Tracker Conventions

- ISO dates (`YYYY-MM-DD`) in every CSV
- Tracker Status set: Queued, Applied, Screen, Interview, Offer, Rejected, Ghosted, Withdrawn
- Every Applied row has a Follow-up Date (+7 days)
- Fill the Outreach columns when outreach is sent (`DIRECT_OUTREACH_WORKFLOW.md`)
- When an application closes (rejected, ghosted after ~4 weeks, withdrawn), move its row to
  `Archive/Job_Application_Tracker_Archive.csv` and its folder to `Archive/`
- Don't bulk-close rows; real outcomes (screens, interviews) must stay visible
- Before starting any application, check the tracker and archive for a previous application to the same company/role

## Interview Prep Rules

- Stories come only from the Source of Truth; confidential work stays capability-level
- AI-run first rounds are common; treat them as real rounds
- Coding rounds that allow AI score how you direct and verify the AI
- Expect identity checks (camera on, ID); offer them up front
- Debrief within 24 hours into `Interview_Notes.md`; update the tracker Status

## Age-Conscious Presentation (if relevant)

- Focus on the last 10-15 years; summarize or omit earlier experience
- Lead with current technologies to show continuous learning
- Omit graduation years if the degree is 15+ years old
- Don't write "decades of experience" or year counts that date the resume; let the roles and dates speak

## Quick Commands Reference

| User Says | Claude Does |
|-----------|-------------|
| "check for jobs" | JOB_SEARCH_WORKFLOW Phase 1 + 2 |
| "which boards should I check?" / "which boards are working?" | JOB_BOARDS_GUIDE setup or Learn From Results |
| "evaluate these jobs" | JOB_EVALUATION_GUIDE |
| "prepare [company] application" | JOB_SEARCH_WORKFLOW Phase 3 |
| "I applied to [company]" | Update tracker (Phase 4) |
| "find the hiring manager at [company]" | DIRECT_OUTREACH_WORKFLOW |
| "prep me for the [company] interview" | Interview prep mode |
| "build my voice profile" | VoiceMatching/README.md |
| "set me up" / "update my targets" | SETUP.md / Search_Profile.md |
| "show queue" / "show tracker" | Summarize the CSV |

## Decisions

When the user settles a question (a kind of role to skip, how to describe a project, a rate), add a
dated line to the Decisions Log in `Search_Profile.md` so no agent asks again. Settings changes go in
the matching `Search_Profile.md` section, never in this file.
