# VoiceMatching - Build a Voice Profile From Your Own Writing

Recruiters reject generic AI prose. This folder is how you give Claude an accurate, evolving reference
for how **you** actually write, so cover letters, outreach emails, application answers and resume
bullets come out sounding like you wrote them.

The idea: collect a large pile of your real, unpolished writing (emails, Reddit, Facebook, Slack...),
let Claude analyze it, and distill it into one condensed **voice profile** of rules and patterns.
Agents drafting for you load only the profile, never the raw pile.

```
VoiceMatching/
|-- README.md                      # this workflow (tracked)
|-- Example_Voice_Profile.md       # the profile template (tracked)
|-- Voice_Samples.md               # index of your raw sources (git-ignored)
|-- Voice_Profile.md               # your distilled profile - what agents load (git-ignored)
|-- raw/                           # your exported writing (git-ignored, never committed)
```

Everything except the two tracked files is git-ignored. Raw exports contain other people's names and
your private life; keep them off any remote.

---

## Step 1: Collect Your Writing

Aim for variety across audiences (professional, recruiter, casual, technical, public) more than raw
volume. Only text **you wrote yourself**, ideally before you started using AI to write it. Put each
export in `VoiceMatching/raw/`.

| Source | How to get it | What you get |
|---|---|---|
| **Sent email** (best for professional voice) | Google Takeout -> Mail -> select only the "Sent" label; or Outlook: export the Sent Items folder. Or copy-paste 30-50 sent emails into `raw/emails.txt` | `.mbox` / `.pst`, or a text file |
| **Reddit** | reddit.com/settings/data-request (GDPR/CCPA request; can take up to 30 days) | `comments.csv`, `posts.csv` |
| **Facebook** | Accounts Center -> Your information and permissions -> Download your information -> JSON | `comments.json`, posts |
| **LinkedIn** | Settings -> Data privacy -> Get a copy of your data | `messages.csv`, shares, comments |
| **Discord** | User Settings -> Data and Privacy -> Request all of my data | per-channel `messages` files |
| **X / Twitter** | Settings -> Your account -> Download an archive of your data | `tweets.js` |
| **Slack / Teams** | Workspace exports are admin-only; copy a sample of your own messages by hand | text file |
| **Anything else you wrote** | Old cover letters you wrote yourself, forum posts, blog posts, design docs, text messages | text files |

Export menu paths change; if one has moved, search "[service] download your data".

Label context when you paste by hand, e.g. `--- email to client about scope ---` or
`--- text to a friend ---`. Audience is the most useful thing the analysis can know.

## Step 2: Ask Claude to Build the Index and Profile

Tell Claude:

```
Build my voice profile from VoiceMatching/raw/ following VoiceMatching/README.md.
```

Claude then:

1. **Inventories** every file in `raw/` and writes `Voice_Samples.md`: file, content type,
   audiences, date range, approximate volume, and what's missing (e.g. "no recruiter emails").
2. **Cleans as it reads**: keeps only your own words. It ignores quoted replies, forwarded text,
   signatures, auto-generated messages, and other people's comments in threads. Large files are read
   in chunks and sampled across the whole date range, not just the start.
3. **Runs analysis passes per context** (professional email, recruiter, negotiation, casual,
   technical explanation, public forum, excited about a project, saying no). It analyzes phrasing and
   structure, never opinions: political, religious or health content can show how you build a sentence,
   but its content never enters the profile or any professional output.
4. **Writes `Voice_Profile.md`** from `Example_Voice_Profile.md`: sentence patterns,
   vocabulary (including words you never use), filler phrases, how you explain things, humor, a guide
   per context, cross-contamination rules, your email formula, and how it all applies to resumes and
   cover letters. Each pattern carries a short real example from your writing as evidence.

## Step 3: Validate It (blind test)

A profile is only right if drafts from it need little rewriting. Ask Claude to draft, using only the
profile:

1. A short reply to a recruiter
2. One cover letter paragraph for a real posting
3. A 2-sentence resume summary

Mark everything that sounds off ("I'd never say 'thrilled'", "too long", "I'd open with the point").
Claude turns each correction into a rule in the profile. Repeat until the drafts sound like you.

## Step 4: Keep It Current

- Add new samples to `raw/` when you have them (a slow Reddit export arriving, new emails) and ask
  Claude to "recalibrate my voice profile" - it re-runs the passes and notes what changed
- Whenever a generated draft sounds wrong, tell Claude what was wrong; it updates the profile rule,
  not just that one draft
- Voice drifts. Recalibrate every few months, weighting recent writing more

## How Other Workflows Use the Profile

- **Cover letters, outreach, application answers**: load the profile first; follow its context guide
  for that audience (recruiter vs hiring manager vs casual)
- **Resumes**: the profile's "Applying Voice to Resumes" section plus `RESUME_CRAFTING_GUIDELINES.md`
- **Precedence**: the profile's banned words beat the crafting guidelines' word suggestions; the
  anti-fabrication rules beat everything, including voice
