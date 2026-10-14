# Showpiece Workflow: Job-Aligned GitHub Demo Projects

Turns the gaps found in real job postings into small public projects that prove you can build that
thing, so a resume claim has a repo behind it. Backlog and gap log: `Showpiece_Backlog.md`.

**Cadence:** set one that fits your time, e.g. one a week while employed, 2 to 4 a week while
searching full time. Each one is sized in days, built with AI assistance.

## Critical rules
1. **Honest framing.** A showpiece is a personal demo project. On resumes it goes under KEY PROJECTS
   with its year. Never present it as client, production or professional experience. It may add
   skills to TECHNICAL SKILLS once it exists and is public.
2. **You can walk through it.** Before it counts as done, you must be able to explain every design
   choice and the main code paths without notes. Interviewers will probe it, often live and without AI.
3. **Nothing private goes public.** No employer or client code, data, or anything under NDA. Rebuild
   generic know-how from scratch with public tools and models.
4. **Cost safety on cloud demos.** Set a budget alarm before the first deploy, ship a one-command
   teardown, and prefer plan-only or local runs when they prove the same skill.
5. **No secrets in repos.** Run a secret scanner (e.g. Gitleaks) before the first push. Keys go in
   `.env.example` only.

## Step 1: Log the gaps (every evaluated posting)
When evaluating a posting (`JOB_EVALUATION_GUIDE.md`), list the requirements that aren't in the
source of truth. Add each one to the **Gap Log** in `Showpiece_Backlog.md`:
- Is it a **must-have** (blocks the screen) or a **nice-to-have**?
- Add the company and date. If the gap already exists, increment its count.

## Step 2: Suggest showpieces
For each new or rising gap, propose 1 to 3 ideas in the backlog's Ideas table. A good idea:
- Closes 2 or more logged gaps, using the posting's exact keywords (ATS matching)
- Fits in 0.5 to 3 days of work, on hardware you actually have
- Has something visible: a live demo, a GIF or video, a CI badge, or published eval numbers
- Plays to an existing strength where possible, so it stands out rather than just filling a hole
- Prefers extending a series repo over a new thin repo when the gaps are related

## Step 3: Pick what to build next
Priority = (posting count of the gaps it closes x 2 if any is a must-have) / effort in days. Tie-breakers:
- An active application is waiting on this gap
- It covers a role family not built for yet

Keep a mix across role families; don't build five of the same kind in a row.

## Step 4: Build
Each showpiece is its own repo, not inside this one.

**Definition of done:**
- [ ] Public repo with a license
- [ ] README: what it is and why, stack, one-command run, screenshot or GIF, honest limitations,
      "how it would scale"
- [ ] Tests plus CI with a passing badge; live demo link when feasible
- [ ] 30 to 60 second video or GIF
- [ ] Secret scan clean; rule 2 walkthrough done

## Step 5: Fold it back in
1. **Source of truth:** add an entry under Personal Projects (dates, stack, what it does, measured
   numbers only).
2. Then the resume variants for the role families it targets, then pin it on GitHub if it's a hero piece.
3. Mark the gaps as covered in the Gap Log, and note it in the tracker row of any application it was
   built for.
