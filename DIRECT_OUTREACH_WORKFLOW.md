# Direct Outreach Workflow

The goal: get your resume in front of a human before the ATS buries it.
Apply through the company's official system AND send a direct email to the
hiring manager simultaneously. You're not bypassing their process - you're
making sure someone notices you exist before the pile grows to 800 applicants.

## When to Use This

Run this workflow for all Tier 1 and Tier 2 jobs from JOB_EVALUATION_GUIDE.md.
For Tier 3 generic applications, skip outreach - the juice isn't worth the squeeze.

## Step 1 - Find the Right Person

Target: the engineering manager or team lead the role would report to.
NOT HR. NOT a recruiter. The person who actually feels the pain of the open role.

### LinkedIn Search (manual - Claude cannot browse authenticated LinkedIn)
Search: `[Company Name] engineering manager` or `[Company Name] [relevant tech] lead`
Look for someone whose team would include this role. Check if the job was posted
by a specific person - that person is often the hiring manager.

### Claude Can Search For
Once you identify a name, ask Claude to:
- WebSearch `[Full Name] [Company] email`
- WebFetch hunter.io for the company's email pattern
- Check the person's GitHub profile for a listed email
- Search for their personal site or tech blog

### Hunter.io (free tier)
Fetch `https://hunter.io/search/[companydomain.com]` to get:
- The email format the company uses (e.g. `{first}.{last}@company.com`)
- Known verified emails at that domain

### Email Pattern Construction
Once you have the format and the person's name, construct the address.
Common patterns:
- firstname@company.com
- firstname.lastname@company.com
- f.lastname@company.com
- firstnamelastname@company.com

### Verification
Run the constructed address through a free checker before sending:
- hunter.io email verifier
- NeverBounce single check (free)
A "valid" result means the mailbox exists. Not guaranteed to reach them, but
better than bouncing.

## Step 2 - Draft the Outreach Email

### Rules
- 3-4 sentences maximum - hiring managers delete long emails from strangers
- One specific credential, not a list of everything
- One specific connection to their company or product
- One small ask - a conversation, not a job offer
- Attach resume as PDF

### Template

```
Subject: [Exact Job Title] - [one specific thing about your background]

Hi [First Name],

I just applied for the [Role] through your website and wanted to reach out
directly. [One sentence: specific credential or achievement relevant to their
work - an award, a patent, a well-known former employer, etc.] I noticed
[one specific thing about their product, tech stack, or recent news] and
think my [specific relevant experience] would be directly useful.

Would you have 15 minutes for a call?

[Your Name]
[linkedin.com/in/you] | [github.com/you]
```

### Example (fictional candidate)

```
Subject: Senior Unity Engineer - XR + industrial robotics background

Hi Sarah,

I just applied for the Senior Unity Engineer role through your website and
wanted to reach out directly. I spent 6 years building factory simulation
tools before moving into XR development full-time, and the VR trainer I
built last year is now used on three production lines. I noticed your
platform is targeting industrial training use cases and that's exactly the
intersection I've been working in.

Would you have 15 minutes for a call?

Alex Rivera
linkedin.com/in/alexrivera | github.com/alexrivera
```

### What to Customize Per Email
- The subject line specific detail
- The credential you lead with (match it to what they care about)
- The "I noticed" line - must be specific to their company, not generic
- Everything else can stay close to the template

## Step 3 - Send Both

1. If job came from a job board, check if the same role exists on the company's
   own careers page first - apply directly through the company site when possible
2. Submit the formal application first
3. Send the direct email same day, ideally within the hour
4. Note "Outreach sent" in the tracker immediately

## Step 4 - Update the Tracker

Fill in these columns in Job_Application_Tracker.csv:
- **Outreach Contact**: Full name of person emailed
- **Outreach Email**: Address used
- **Outreach Date**: Date sent
- **Outreach Response**: Any reply (even an auto-reply or OOO)

## Step 5 - Follow Up (Once Only)

If no response after 5-7 business days, one follow-up is acceptable:

```
Subject: Re: [original subject]

Hi [Name], just following up on my note from [date]. Still very interested
in the [Role] - happy to share more if helpful.

[First Name]
```

After one follow-up, move on. Two unreplied emails is the limit.

## Finding Contacts - What Claude Can Do

For any job you're pursuing, ask:
"Find the hiring manager at [Company] for a [Role] position"

Claude will:
1. WebSearch for likely engineering managers at that company
2. WebFetch Hunter.io for the company's email pattern
3. Check GitHub org for team members with public emails
4. Construct the most probable email address
5. Draft a customized outreach email based on the job description

You confirm the person's name via LinkedIn, Claude handles the rest.

## When You Can't Find an Email

Fall back options in order:
1. LinkedIn direct message (shorter than email - 2-3 sentences max)
2. Twitter/X DM if they're active there
3. Reply to a recent post they made on LinkedIn with a brief comment
   then follow up with a DM
4. Skip outreach for this one - not every application needs it

## Notes on Tone

The email should sound like the user wrote it in 5 minutes (match their voice profile), not like it was
AI-crafted. Short, direct, confident without overselling. The credential
and the "I noticed" line do the work - everything else should get out of
the way.

Do not use: "I am reaching out to express my interest", "I am excited about
the opportunity", "I believe I would be a great fit". These are ATS phrases
that make humans cringe too.

Do use: direct statements, specific details, a small ask.
