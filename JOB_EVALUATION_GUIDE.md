# Job Evaluation Guide

Use this when the user provides a list of job links or postings to evaluate.
Goal: quickly filter out disqualifying roles, tier the rest, and decide which to apply for.

## Where the User's Criteria Live

This guide is the method. The user's own criteria are in `Search_Profile.md`: read it before
evaluating anything. Sections used here: Location and Work Authorization, Compensation, Automatic
Disqualifiers, Flag for the User, Scoring Adjustments, Target Role Families and Base Resumes.

## Automatic Disqualifiers - Skip Immediately

- Everything under `Search_Profile.md` @ Automatic Disqualifiers
- Location or work-authorization blockers (see Location Rules)

## Flag for the User (don't auto-apply, don't auto-skip)

Categories listed under `Search_Profile.md` @ Flag for the User are judgment calls: put them in the
FLAG FOR USER group with the reason, and record the user's answer in the Decisions Log. Also watch for
postings that obscure who the end client is when the user has company exclusions.

## Location Rules

- Compare the posting against `Search_Profile.md` @ Location and Work Authorization
- "Remote (US)" often means US residents only, and "Remote" with a country list means only those
  countries. Check the location restriction before scoring
- When the posting is ambiguous, say so in "Watch for" rather than guessing

## Compensation

Compare any listed range against `Search_Profile.md` @ Compensation:
- At or above target: no adjustment
- Between minimum and target: no deduction, but note it in the evaluation
- Below minimum: -10 points unless the role is an exceptional fit

## Tier System

### Tier 1 - Apply Immediately (Score 50+)
- Meets your location/remote requirement
- Tech match: the user's primary skills (`Search_Profile.md` @ Scoring Adjustments)
- Recent skills: their current-focus skills
- Domain: domains they have real experience in
- No blockers

### Tier 2 - Worth Customizing (Score 35-49)
- The user's secondary skills are the primary requirement
- Similar but not exact technology match
- An industry you could credibly move into

### Tier 3 - Generic Application (Score 20-34)
- General software engineering
- Your skills are "nice to have", not required

### Skip
- Any automatic disqualifier
- Score below 20

## Scoring Matrix

**Technical Fit (0-5 points each)**
- Languages match (Source of Truth @ Technical Skills)
- Platform/framework match
- Domain match
- Modern tech alignment

**Practical Fit (0-10 points each)**
- Remote work / location confirmed
- No clearance or visa sponsorship needed
- Timezone compatible

**Bonus Points (+5 each)**
- Each bonus listed in `Search_Profile.md` @ Scoring Adjustments

**Red Flag Deductions (-10 each)**
- Requires relocation
- Mandatory travel
- Legacy tech only
- Any extra red flags listed in `Search_Profile.md` @ Scoring Adjustments

**Score Interpretation**
- 50+: Tier 1 - Apply immediately
- 35-49: Tier 2 - Customize and apply
- 20-34: Tier 3 - Generic application if time permits
- <20: Skip

## Hire Odds and Ghost Risk

Fit score says how well the role matches you. These two say whether applying is worth the time,
and they set the order of `Job_Search_Queue.csv` (best Hire Odds first, then lowest Ghost Risk).

- **Hire Odds (A best .. D worst)**: fit, how likely you pass the screen, visa/entity friction,
  seniority stretch, and how many applicants it will draw
- **Ghost Risk (1 low .. 5 high)**: posting older than 60 days, reposted repeatedly, vague
  "talent pool" or "future openings" wording, no named team or manager

## Keyword Signals

**Green Flags - Apply Fast**
- The green-flag keywords in `Search_Profile.md` @ Scoring Adjustments
- Remote-first, Distributed team, Work from anywhere

**Yellow Flags - Investigate Further**
- "Hybrid" - check if truly flexible
- "Preferred location" - often negotiable
- "Nice to have clearance" - may not be required
- "Travel occasionally" - define occasionally

**Red Flags - Usually Skip**
- On-site required, Must be local
- Active clearance required
- Extensive travel (>25%)
- Legacy systems only

## Output Format

When evaluating a list of jobs, respond with:

```
TIER 1 - Apply Immediately:
1. [Job Title] at [Company] - Score: XX | Hire Odds: X | Ghost Risk: X
   Matches: [2-3 strongest alignments]
   Watch for: [any concerns]
   Showpiece gaps: [gap (must/nice) -> existing idea ID or "new idea"]

TIER 2 - Worth Customizing:
1. [Job Title] at [Company] - Score: XX
   Matches: [list]
   Gaps: [skills to emphasize or downplay]
   Showpiece gaps: [...]

TIER 3 - Generic Application:
1. [Job Title] at [Company] - Score: XX
   Apply with: [base resume variant]

FLAG FOR USER:
1. [Job Title] at [Company] - Why: [the judgment call]

SKIP:
1. [Job Title] at [Company] - Reason: [clearance / on-site / location / etc]
```

## Gaps -> Showpieces

For every Tier 1 or Tier 2 role, list its requirements that aren't in the source of truth. Mark each
as must-have or nice-to-have and add it to the Gap Log in `Showpiece_Backlog.md` (process:
`SHOWPIECE_WORKFLOW.md`). A missing skill isn't automatically a reason to skip a role: gaps matter
at the screen, and showpieces close them honestly. Never add a gap skill to the resume itself.

## Application Strategy

Evidence from 2026 hiring data: cold applications convert at roughly 0.3-0.5%, referrals convert
about 11x better than cold inbound, and applying within 24-72 hours of posting matters. So:

1. Prefer fewer, tailored applications (roughly 10-15 a week) over volume. No auto-apply bots.
2. Pair every Tier 1/2 application with outreach (`DIRECT_OUTREACH_WORKFLOW.md`) or a referral ask
3. Apply on the company's own careers page (Greenhouse/Lever/Ashby) rather than through an aggregator

For a batch of Tier 1 and Tier 2 roles:

1. Group by primary skill needed
2. Select the closest base resume for each group
3. Per application, change only: summary, skill order to match the posting, and the 1-2 project
   descriptions most relevant to the role
4. Cover letter: start from your general letter, customize the intro and one body paragraph
5. Track each in `Job_Application_Tracker.csv`

## Base Resume Selection

Use the base resume mapped to the posting's role family in `Search_Profile.md` @ Target Role Families
and Base Resumes. If a posting spans two families, start from the closer one and pull the 1-2 most
relevant bullets from the other (same facts, Source of Truth wording).
