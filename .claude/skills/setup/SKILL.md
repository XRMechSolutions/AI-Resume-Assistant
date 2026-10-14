---
name: setup
description: Walk the user through setting up their job-search workspace - explain what's needed from them, create their personal files, interview them, build their Source of Truth, search profile, base resumes, voice profile and board list. Use when the user runs /setup, says "set me up", or when CLAUDE.md Step 0 finds setup incomplete.
---

# Setup: build the user's job-search workspace

The full procedure is `SETUP.md` (section "For the agent: the onboarding procedure"). Read it now and
follow it. This skill adds how to open the conversation and how to keep it moving.

## 1. Check where they are

Read `Search_Profile.md` if it exists.
- **Missing**: this is a fresh start. Go to step 2.
- **Exists, setup incomplete**: say which Setup Status boxes are done, which step is next, and ask
  whether to continue there. Skip step 2 unless they ask what's needed.
- **Setup complete**: tell them, and ask what they want to change (experience, targets, base resumes,
  voice profile, boards). Route to the matching `SETUP.md` step or `CLAUDE.md` mode.

## 2. Open with what you need from them

Before creating anything, give a short overview in plain language:

**What this sets up:** a verified record of your experience that every resume is built from (so
nothing gets made up), your job-search settings, 2-6 base resumes, a profile of how you write, and a
list of job boards worth checking. About 1-2 hours total; it can be split across sessions, and it
picks up where you left off.

**What helps to have ready (all optional, everything can be typed in instead):**
- Your current or recent resumes (any format) and your LinkedIn profile (Save to PDF, or paste the text)
- A list of projects, with links to anything public (GitHub, demos, videos)
- Certifications, patents, publications, awards
- Some of your own writing for the voice profile: sent emails are best (VoiceMatching/README.md
  explains how to export them); this step can wait until later

**Decisions you'll be asked about:**
- What kinds of roles you want (role families) and which you'd rather skip
- Where you can work from, work authorization, remote/hybrid/on-site
- Pay: your target and your floor, for salary and/or contract
- Deal-breakers (clearance, travel, industries you won't work in)
- Anything under NDA, and how much you're allowed to say about each employer or client
- Whether to use the optional job-board search tool (job_mcp) - it has an account-flag risk on
  logged-in boards, which you'll get to decide on

**How it stays honest:** only things you tell or show me go into your record. Anything uncertain gets
parked as unconfirmed and is never used until you confirm it. Old resumes are treated as claims to
check, not facts.

Then ask: "Want to start by pasting your resume or LinkedIn profile, or would you rather I ask the
questions from scratch?"

## 3. Run SETUP.md, steps 1-9

- Create the personal files first (Step 1) and confirm with `git status` that none of them shows as
  a new file to commit
- Ask a few questions at a time. Save answers to `Questionnaire_Answers.md` as you go
- After each step: tick its box in `Search_Profile.md`, say what was created, say what's next, and
  offer a natural stopping point ("good place to stop - say /setup next time and we'll continue")
- Never fill a gap with a plausible guess; log it in `Unconfirmed_Facts.md` and ask

## 4. Finish

When every box is ticked (or marked skipped), set `Setup status: **complete**`, summarize what exists
now, and suggest a first real task: paste a job posting, or "check for jobs".
