# AI Resume Assistant

An AI-assisted job search system for Claude Code. It helps you:

- **Tailor resumes** to specific jobs without fabricating experience
- **Write in your own voice** using a voice profile built from your real writing
- **Find jobs** across boards, work out which boards are worth checking, and rank what you find
- **Evaluate opportunities** against your skills, location, pay floor and deal-breakers
- **Reach hiring managers** directly alongside each application
- **Track everything**: queue, applications, follow-ups, outreach, interviews, skill gaps
- **Generate ATS-safe PDFs and Word files** from plain text resumes

## How It Works

`CLAUDE.md` is the router for every agent working in the repo,
including ones started inside a `JobSearches/` application folder. Codex and Gemini CLI reach it
through the tracked `AGENTS.md` and `GEMINI.md` pointers. It sets the hard rules (never invent
experience, edit the source then derive, sound like you), tells Claude which guide to load for each
kind of task, and defines the Pre-Send Check every outgoing document must pass. It has no personal
content: your settings go in `Search_Profile.md` and your facts in `Source_of_Truth.md`, both created
during setup and git-ignored. The guides hold the detail:

| Guide | What it covers |
|---|---|
| `RESUME_CRAFTING_GUIDELINES.md` | Human-sounding resumes, generation traps, standing out, ATS optimization |
| `RESUME_TXT_FORMAT.md` | The exact .txt format `create_pdf.py` parses |
| `JOB_EVALUATION_GUIDE.md` | Disqualifiers, tiers, scoring, Hire Odds / Ghost Risk, pay parameters |
| `JOB_SEARCH_WORKFLOW.md` | Discover -> review -> prepare -> apply -> track |
| `JOB_BOARDS_GUIDE.md` | How Claude picks your boards, sets check frequency, and learns which ones work |
| `DIRECT_OUTREACH_WORKFLOW.md` | Finding and emailing the hiring manager |
| `SHOWPIECE_WORKFLOW.md` | Turning repeated skill gaps into small public demo projects |
| `VoiceMatching/README.md` | Building your voice profile from your own emails and posts |
| `job_mcp/README.md` | Optional MCP server: board search + application filling (never submits) |

## Quick Start

```bash
git clone https://github.com/XRMechSolutions/AI-Resume-Assistant.git
cd AI-Resume-Assistant
pip install -r requirements.txt
```

Open your agent in the folder and run **`/setup`** (Claude Code) or say **"set me up"** (any agent).
It tells you what it needs from you (old resumes, LinkedIn, project list, a few decisions about
roles, location and pay), then interviews you and builds everything: your Source of Truth, search
profile, base resumes, voice profile and board list. See `SETUP.md` for the steps; it takes 1-2 hours
and can be spread over several sessions.

`reportlab` builds PDFs, `python-docx` builds Word files, `pymupdf` checks page counts. The rest of
`requirements.txt` is only for the optional `job_mcp` server.

After setup:

```
> Here's a job description for a Senior Backend Developer at TechCorp...
```

The agent checks your Source of Truth, verifies every claim, tailors a resume in your voice, renders
it, and writes `Prep_Notes.md` with the form answers, honest gap framing, and the Pre-Send Check.

## File Structure

```
AI-Resume-Assistant/
├── CLAUDE.md                     # Router + rules for every agent (shared, no personal content)
├── AGENTS.md / GEMINI.md         # Point Codex / Gemini CLI at CLAUDE.md
├── SETUP.md                      # Onboarding the agent runs with you
├── .claude/skills/setup/         # The /setup skill (Claude Code)
├── README.md
├── RESUME_CRAFTING_GUIDELINES.md / RESUME_TXT_FORMAT.md
├── JOB_EVALUATION_GUIDE.md / JOB_SEARCH_WORKFLOW.md / JOB_BOARDS_GUIDE.md
├── DIRECT_OUTREACH_WORKFLOW.md / SHOWPIECE_WORKFLOW.md
├── create_pdf.py                 # .txt -> PDF (and .docx with --docx)
├── create_cover_letter_docx.py
├── Job_Boards.csv                # Public board list with tiers and API notes
├── requirements.txt
├── VoiceMatching/                # Voice profile workflow + template
├── job_mcp/                      # Optional job-search MCP server
├── examples/                     # Starting points setup creates your files from, + the questionnaire
│
└── [Personal - created by setup, git-ignored]
    ├── Search_Profile.md, Source_of_Truth.md, Questionnaire_Answers.md
    ├── ANTI_FABRICATION_CHECKLIST.md, Unconfirmed_Facts.md, Application_Responses.md
    ├── VoiceMatching/raw/, VoiceMatching/Voice_Profile.md
    ├── Job_Application_Tracker.csv, Job_Search_Queue.csv, Open_Calls.csv, Job_Boards_Ranked.md
    ├── Showpiece_Backlog.md, PORTFOLIO_READINESS.md, Project_Demo_Videos.md
    ├── *Resume*.txt / .pdf / .docx, *CoverLetter*
    ├── JobSearches/<Company>_<Role>/   # JD, tailored resume, letter, Prep_Notes.md, Interview_Notes.md
    └── Archive/                         # Closed applications
```

## Key Concepts

### Source of Truth
The only authority for what goes on a resume. Anything not in it doesn't get claimed. Facts you're
not sure about yet go in `Unconfirmed_Facts.md` until you confirm them.

### Anti-Fabrication Checklist
What you do and don't know, plus a log of corrections every time Claude gets something wrong, so
the same mistake never repeats.

### Voice Profile
Condensed rules for how you write, distilled from your real emails and posts. Cover letters and
outreach that sound like you beat polished AI text.

### Job Evaluation
Each posting gets a fit score and tier, plus Hire Odds (A-D) and Ghost Risk (1-5), which set the
order you apply in. Unmet requirements go into a Gap Log; gaps that keep recurring become small demo
projects ("showpieces") that close them honestly.

### Board Strategy
Claude builds your board list for your field and region, checks each on a cadence, and re-ranks boards
by which ones actually produce screens.

## PDF Generation

```bash
python create_pdf.py "Your_Resume.txt"                  # single file
python create_pdf.py "Your_Resume.txt" --docx           # also write a Word copy
python create_pdf.py "Your_Resume.txt" --verbose        # show parsed sections
python create_pdf.py                                    # every *Resume*.txt in the folder
```

Unrecognized ALL-CAPS headers print a `[WARN]`, since an unrecognized section is silently dropped
from the PDF. Format rules: `RESUME_TXT_FORMAT.md`.

## Contributing Improvements

When you improve the workflow in your own copy and want to share it:

1. Make and test the improvement in your personal files
2. Extract the logic (not personal data) into the tracked files: `CLAUDE.md`, `SETUP.md`, the
   guides, `examples/` starting points, or scripts. Personal settings belong in `Search_Profile.md`,
   never in a tracked file
3. Commit and push only tracked files

**Share:** workflow sections, evaluation criteria, anti-fabrication rules, board notes, script fixes.
**Don't share:** contact info, your experience, application history, voice samples, source of truth.

## Tips for Best Results

1. **Be thorough in your Source of Truth** - the more detail, the better the tailoring
2. **Update it first** - new project or skill? Source of Truth, then base resumes
3. **Be honest about skill levels** - "familiar" vs "expert"
4. **Only real numbers** - documented metrics are gold; invented ones are fabrication
5. **List what you DON'T know** - it prevents accidental fabrication
6. **Correct Claude in the files** - when a draft sounds wrong or claims something false, have Claude
   add the rule to the voice profile or the checklist's Known Corrections

## License

MIT - Feel free to use, modify, and share.
