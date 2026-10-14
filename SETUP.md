# SETUP - Getting Started

## For the person (3 steps)

1. Clone the repo and install the Python packages:
   ```bash
   git clone https://github.com/XRMechSolutions/AI-Resume-Assistant.git
   cd AI-Resume-Assistant
   pip install -r requirements.txt
   ```
2. Open your AI agent in this folder (Claude Code: `claude`; Codex and Gemini CLI also work).
3. Say: **"set me up"**.

The agent interviews you, builds your files, and creates your base resumes. Plan on 1-2 hours,
which can be spread over several sessions; it picks up where you left off. Have your old resumes,
LinkedIn profile and any project lists handy; pasting them in saves a lot of typing.

Everything personal it creates is git-ignored, so your data never gets committed.

---

## For the agent: the onboarding procedure

Run these steps in order. Progress is tracked in the Setup Status checklist at the top of
`Search_Profile.md`: tick each box as its step finishes, and on a new session resume at the first
unticked box. Talk to the user plainly; ask a few questions at a time, never all at once.

**Ground rules for the whole setup**
- Record only what the user tells you or shows you. Never fill a gap with a plausible guess; when
  something is uncertain, put it in `Unconfirmed_Facts.md` and move on.
- Keep the user's own words where you can. Their phrasing feeds the voice profile.
- After each step, tell the user what was created and what's next.

### Step 1: Create the personal files

Create any that are missing at the repo root (never overwrite an existing one):

| Create | From |
|---|---|
| `Search_Profile.md` | `examples/Example_Search_Profile.md` |
| `Source_of_Truth.md` | `examples/Example_Source_of_Truth.md` |
| `ANTI_FABRICATION_CHECKLIST.md` | `examples/Example_Anti_Fabrication_Checklist.md` |
| `Unconfirmed_Facts.md` | `examples/Example_Unconfirmed_Facts.md` |
| `Application_Responses.md` | `examples/Example_Application_Responses.md` |
| `Job_Application_Tracker.csv`, `Job_Search_Queue.csv`, `Open_Calls.csv` | `examples/*_Template.csv` |
| `Job_Boards_Ranked.md` | `examples/Job_Boards_Ranked_Template.md` |
| `Showpiece_Backlog.md` | `examples/Example_Showpiece_Backlog.md` |
| `PORTFOLIO_READINESS.md`, `Project_Demo_Videos.md` | `examples/Portfolio_Readiness_Template.md`, `examples/Project_Demo_Videos_Template.md` |
| `JobSearches/`, `Archive/` | empty folders |

Run `git status` afterwards: none of these should show as new files. If one does, stop and fix
`.gitignore` before going further.

### Step 2: Interview

Walk through `examples/Setup_Questionnaire.md` section by section. Save the answers verbatim to
`Questionnaire_Answers.md` as you go (that file is the resume point if the session ends).

- Offer the shortcut first: "Paste your current resume / LinkedIn profile and I'll pre-fill what I
  can, then ask about the rest." Treat pasted resumes as claims to confirm, not facts: older resumes
  are often where fabrications started.
- Section H (DO NOT CLAIM) and Section K (gaps, uncertainty) matter most. Don't rush them.
- If the user prefers, they can fill in the questionnaire themselves and tell you when it's done.

### Step 3: Build the Source of Truth

Turn the answers into `Source_of_Truth.md` following its template structure. Then go through it
with the user, role by role, and ask them to confirm or correct each section. Remove anything they
couldn't prove if asked; move anything uncertain to `Unconfirmed_Facts.md`.

Then fill `ANTI_FABRICATION_CHECKLIST.md`: technologies they have (by level), technologies and
experiences to never claim, verified achievements.

### Step 4: Fill in the Search Profile

Fill every section of `Search_Profile.md` from the interview (Section I covers most of it), asking
for anything missing: contact header, target role families, location and work authorization, pay
floor and target, deal-breakers, judgment-call categories, confidentiality rules per employer, and
hardware for demo projects. Record decisions they make along the way in the Decisions Log.

### Step 5: Base resumes

Agree on 2-6 role families (one base resume each), then for each:
1. Write `<Name>Resume_<Variant>.txt` following `RESUME_TXT_FORMAT.md` and
   `RESUME_CRAFTING_GUIDELINES.md`, using only the Source of Truth
2. Render with `python create_pdf.py "<Name>Resume_<Variant>.txt"`; fix every `[WARN]` until it renders
   clean at 2 pages or less
3. Run the Pre-Send Check in `CLAUDE.md` and show the user the PDF

Add the role family -> base resume -> search keywords rows to `Search_Profile.md`.

### Step 6: Voice profile

Explain `VoiceMatching/README.md` and ask the user to export some of their own writing into
`VoiceMatching/raw/` (sent email is the most useful). This can happen later: if they want to skip
for now, note it in the checklist and use their questionnaire Section J answers as a stand-in.
When samples are there, build `VoiceMatching/Voice_Profile.md` and run the blind test.

### Step 7: Job boards and target companies

Follow `JOB_BOARDS_GUIDE.md` @ First-Time Setup: pick their boards, set check frequencies, write
search terms per role family into `Job_Boards_Ranked.md`, and start a target company list.

### Step 8: Optional - job-search MCP

Offer the `job-search` MCP server (`job_mcp/README.md`). Explain what it does and the account-flag
risk of the logged-in boards before enabling any. Skipping it is fine; note the choice.

### Step 9: Finish

Set `Setup status: **complete**` in `Search_Profile.md`. Then tell the user the everyday commands
(`CLAUDE.md` @ Quick Commands Reference) and suggest a first real run: "paste a job posting you're
interested in" or "check for jobs".

---

## Later changes

- New job, project or skill: "update my experience" - the agent edits `Source_of_Truth.md` first,
  then the base resumes (Hard Rule 3 in `CLAUDE.md`)
- New targets, pay floor, or deal-breaker: "update my search profile"
- Drafts don't sound like you: "that doesn't sound like me, here's why" - it becomes a voice profile rule
- Claude claimed something false: tell it - it goes into Known Corrections in the checklist so it never repeats

## Troubleshooting

| Problem | Fix |
|---|---|
| The agent adds skills you don't have | Make the DO NOT CLAIM list in `Source_of_Truth.md` more complete, and add the mistake to Known Corrections in `ANTI_FABRICATION_CHECKLIST.md` |
| Resumes sound AI-generated | Build or recalibrate the voice profile; check `RESUME_CRAFTING_GUIDELINES.md` §11 traps |
| PDF formatting is off | `python create_pdf.py "file.txt" --verbose`, fix every `[WARN]`, compare against `RESUME_TXT_FORMAT.md` |
| The agent ignores your documents | Ask "show me where in Source_of_Truth.md that is documented" - if it can't point to the line, remove the claim |
| The agent keeps sending you to setup | Finish the unchecked items in `Search_Profile.md` @ Setup Status, or mark skipped ones as skipped |
