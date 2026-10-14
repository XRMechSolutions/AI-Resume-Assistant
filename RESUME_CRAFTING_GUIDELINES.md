# Resume Crafting Guidelines - Human-Authentic Style

## Core Principle
Write resumes as if the user carefully crafted them - professional and thoughtful, but with the natural voice and subtle variations that distinguish human writing from AI-generated content. The goal is competent and polished, not rushed, but also not artificially perfect.

## 1. Language & Word Choice

### NEVER Use These AI Marker Words
- **Corporate AI speak**: leverage, utilize, spearhead, orchestrate, robust, seamless, cutting-edge, innovative, revolutionary
- **Transition words**: moreover, furthermore, additionally, consequently, thus
- **Emotional/subjective**: passionate, excited, thrilled, eager, dedicated
- **Overused descriptors**: crucial, pivotal, meticulous, comprehensive, extensive, profound
- **AI favorites**: delve, realm, tapestry, landscape, foster, ensure, pertaining to

### DO Use Simple, Direct Language
- "Used" instead of "utilized" or "leveraged"
- "Built" instead of "developed innovative solutions"
- "Fixed" instead of "resolved critical issues"
- "Led" instead of "spearheaded"
- "Connected" instead of "orchestrated integration"
- "Made" instead of "created" sometimes
- "Got working" instead of "successfully implemented"

### Natural Technical Descriptions
- State tools/languages without justification: "Python" not "powerful Python programming language"
- Mix formal and informal: "Built backend API" and "Got the robots talking to each other"
- Spell out a technical acronym once, then use the acronym: "Kotlin Multiplatform Mobile (KMM)" (ATS may search for either form)
- Include specific version numbers and tools: "Unity 2021.3", "ABB RobotStudio 6.08"

## 2. Sentence Structure & Flow

### Vary Sentence Patterns
- Mix complete and incomplete sentences
- Sometimes start with the object: "Factory dashboard built to track KPIs"
- Use fragments for impact: "Patent holder." or "Remote work only."
- Combine related items sometimes: "Built and deployed tracking system"
- Don't always start with action verbs

### Realistic Bullet Points
- **Inconsistent length**: Some short, some long (in the .txt every bullet is still a single line - see `RESUME_TXT_FORMAT.md`)
- **Varying detail**: More detail on interesting projects, less on routine work
- **Not all parallel**: Mix structures within same job
- **Occasional combined thoughts**: "Developed Python scripts for data analysis and also helped with Excel reports"

### Example Natural Progression
Instead of perfect parallel structure:
```
BAD (AI-style):
• Developed comprehensive data pipeline for processing
• Implemented robust error handling for system stability
• Created detailed documentation for team knowledge transfer

GOOD (Human-style):
• Built data pipeline in Python to handle sensor data
• Added error handling after it crashed during a demo
• Documentation written for the next person who has to fix this
```

## 3. Natural Variation, Not Deliberate Errors

What makes a resume read as AI-written is uniformity: every bullet the same shape, every claim
inflated, every line keyword-optimized. Fix that with varied structure and real detail, never with
planted mistakes.

### Never Add Deliberate Errors
- No intentional typos, double spaces, or mixed bullet styles - they break the PDF parser
  (`RESUME_TXT_FORMAT.md`) and look careless to a human reader
- Spell product and tool names exactly one way, the official way ("FANUC ROBOGUIDE", "Node.js").
  ATS matches exact names; a variant spelling is a missed keyword

### Natural Human Patterns
- Put the most relevant project first for this job
- More detail on complex or interesting projects, less on routine work
- Vary bullet openings and structure within a job
- Present tense for the current role, past tense for everything else

## 4. Content & Details

### Specificity Without Perfection
- Use only numbers that are documented in the source of truth, exactly as documented. Never
  adjust a number to make it look more "real" (47 instead of 50) - that is fabrication
- Include specific technical details: "0.001mm precision", "130 dialects"
- Mention actual constraints: "2GB+ file size limitations"
- Reference specific tools/versions: "Unity 2021.3.18f1", "ABB RobotStudio 6.08"

### Authentic Technical Descriptions
- State what you did, not why it matters
- Include mundane tasks among impressive ones
- Mention technical solutions: "Implemented custom networking to overcome hardware limitations"
- Reference real constraints: "Had to work around Windows 10 compatibility"

### Examples of Natural vs AI Writing

**AI Style**: "Leveraged advanced computer vision algorithms to enhance quality inspection processes, resulting in significant improvement in defect detection accuracy"

**Human Style**: "Built OpenCV-based inspection system that caught 97% of defects in testing" (only if that number is documented)

**AI Style**: "Architected scalable microservices infrastructure utilizing cloud-native technologies"

**Human Style**: "Built Node.js backend on Digital Ocean, refactored to microservices architecture for scalability"

## 5. Formatting Guidelines

Layout is fixed by the .txt format the PDF generator parses (`RESUME_TXT_FORMAT.md`), and that
format wins over any advice here. Within it:

- Use `•` for bullets everywhere (a `- ` item only under a `Heading:` sub-section)
- Keep bullets in a job contiguous - a blank line ends the bullet group
- Skills section doesn't need perfect categorization
- Don't alphabetize lists; order skills by what the job asks for

## 6. The Professional Balance

### What We Want
- **Carefully written** but not artificially polished
- **Professional throughout** with occasional personality
- **Technically precise** without unnecessary jargon
- **Natural variations** in structure and word choice
- **Thoughtful organization** that isn't perfectly symmetrical

### The Right Mix
- 95% professional, polished content
- 5% natural human elements:
  - Slight variations in bullet structure
  - Varying levels of detail based on project interest/complexity
  - Natural word choices over corporate speak

### What This Looks Like
- "Developed comprehensive testing framework" → "Built testing framework covering core functionality"
- "Leveraged cutting-edge technology" → "Used React Native for cross-platform development"
- "Spearheaded initiative" → "Led migration to microservices architecture"
- Perfect parallel bullets → Mix of starting words and structures

## 7. Final Checklist

Before finalizing any resume, verify:

1. **Professional tone throughout?** Would this impress a hiring manager at a tech company?
2. **Natural language patterns?** Direct verbs, varied sentence structure, no AI markers
3. **Natural variation?** Bullets vary in shape and detail; no deliberate typos or formatting errors
4. **Technical accuracy?** Specific tools, versions, and metrics without embellishment
5. **Balanced detail?** More detail on complex/interesting projects, less on routine work
6. **Authentic voice?** Sounds like an experienced engineer wrote it, not a content generator
7. **Clear and compelling?** Easy to read, highlights real achievements without overselling
8. **Would pass the "colleague test"?** If a former colleague read this, would they recognize it as accurate?

## 8. Voice Calibration Examples

### Natural Writing Style:
- "Developed tool" not "Developed innovative solution"
- "50+ machines" not "numerous manufacturing systems"
- "Patent holder" not "Holds patent for innovative process"
- "Built with Python" not "Utilized Python to construct"
- "Remote work only" not "Exclusively seeking remote opportunities"

## 9. Common Traps to Avoid

### The Optimization Trap
Don't optimize every bullet for keywords. Some bullets should just state what you did.

### The Impact Trap
Not everything needs metrics or business impact. Sometimes you just fixed something.

### The Buzzword Trap
Resist adding trendy terms. If you did machine learning, say "machine learning" not "leveraged AI/ML to drive innovation"

### The Perfection Trap
What reads as AI is uniformity: perfectly parallel bullets, a metric on every line, buzzwords everywhere. Clean formatting is fine; vary the structure and keep the details real.

## 10. Remember the Source

The truth documents are the user's brain dump - they're already in their natural voice. When crafting resumes:
1. Pull directly from truth documents when possible
2. Keep their phrasing style
3. Don't "upgrade" their language
4. Maintain their level of technical detail
5. Preserve their way of describing projects

## Application

When creating any resume:
1. Start with content from truth documents
2. Organize for the specific role
3. Apply these guidelines for authentic voice
4. Check every bullet against the traps in section 11
5. Read aloud to verify it sounds human
6. Run the Pre-Send Check in CLAUDE.md

The goal: A resume that looks like the user spent 30 minutes customizing their standard resume for this job, not like ChatGPT wrote it from scratch.

## 11. Resume Generation Traps

Patterns that show up again and again in AI-tailored resumes. Each one either breaks the user's
voice or crosses into fabrication.

### Power Verb Inflation
These verbs come from resume guides, not from people:
- "Implemented" - say "Built", "Set up", or "Added"
- "Architected" - say "Built", "Set up", or "Designed"
- "Developed" (when vague) - say "Built" or name the specific thing
- "Spearheaded", "Orchestrated", "Championed" - never use these

### Section Stretching (Fabrication Risk)
When tailoring for a role, there's a pull to reframe unrelated work to fit the narrative: VR work
described as "robotics simulation", general software work described as "mobile development".
**Rule: if the work has to be described in completely different words to fit the resume focus, it
doesn't belong on that version. Leave it out or describe what it actually was.**

### Fabricated Project Blocks
Never create project entries that aren't in the source of truth, even when the skills are
plausible. If a project isn't documented, it doesn't go on the resume.

### Undocumented Metrics
- A time saving, percentage or count that isn't in the source of truth - cut it
- A self-assessment presented as a measurement ("9.5/10 realism") - cut it
- A platform's target spec presented as an achievement ("stable 72fps" when that's the device default) - cut it
- **Rule: if you can't point to where the number came from, cut it**

### Vague Filler Bullets
"Real-time monitoring for production systems", "Large dataset processing and optimization" -
these could be on anyone's resume. **Rule: every bullet names a specific technology, project, or
measurable detail.**

### Adjective Self-Description in Summaries
"Versatile software engineer", "proven track record", "delivering complex solutions from concept to
deployment". **Rule: the summary lists facts about the work, not adjectives about the person.**

### Corporate Language
- "Led enterprise tool adoption affecting 3 sites" - say "Led the tool rollout across 3 sites"
- "Consistent remote delivery since 2021" - say "Working remotely since 2021"

### Claiming Expertise
Don't write "expert at X". Show it: "Spent the last 4 years connecting hardware (trackers,
scanners, serial devices) to Unity". Let the reader conclude "expert" from the evidence.

## 12. Standing Out in an AI-Saturated Pool

Most applicants use AI to write resumes. To stand out, use details only this candidate could know.
Pull them from the source of truth; its "Notes for Resume Customization" section is a good place to
keep the user's strongest ones.

### Proof-of-Work Details
Specific technical obstacles and how they were handled can't be faked:
- "Rewrote the vendor's model-splitting tool to handle 2GB+ files"
- "Built tracking-loss detection before the SDK supported it"
Include 1-2 of these per resume.

### Unique Skill Combinations
Highlight combinations that are genuinely rare in the market (e.g. game engine + industrial robotics,
enterprise background + current AI work). List the user's in the source of truth.

### Specific Numbers Over Generic Percentages
- "Reduced scanning time from 3.5 hours to 1 hour" beats "improved performance by 50%"
- "Led the robotics community of practice across 3 sites" beats "managed large team"
Only numbers from the source of truth, as always.

### The Story Arc
A short narrative of intentional career progression (e.g. enterprise credibility -> startup agility ->
current specialty). Use it when a summary or cover letter needs a story.

### The Ultimate Test Before Sending
1. Could any other applicant have written this exact resume?
2. Does it contain at least 3 details only this candidate would know?
3. Does it tell a coherent story, not just list skills?
4. Would a human reader remember something specific about it?

If any answer is no, add more specific details from the source of truth.

## 13. Per-Application Customization

### Phase 1 - Parse the Job Description
1. Extract the exact job title and use it in the summary
2. Identify the 3-5 most emphasized skills (usually repeated)
3. Note any unusual requirements (specific frameworks, domains)

### Phase 2 - Strategic Matching
- Use their EXACT phrasing when truthful: "Node.js" not "NodeJS", "REST APIs" not "RESTful services"
- Choose 2-3 projects that best match their industry and tech stack
- Reorder skills to match their priority order (only skills the user has)

### Phase 3 - The Extra Mile
Add one element showing you understand their specific needs:
- Reference their actual product or industry challenge
- Connect a specific project to their tech stack
- Include a side project that aligns with their mission

### Cover Letter Approaches That Work
- "I Built Something Like Yours": "I noticed you use [tech]. In [project] I built a similar [feature]..."
- "I Solved Your Exact Problem": describe a specific technical challenge that matches their pain point
- "Future Vision": reference their recent announcement or blog and connect your experience to it

Always add one unique sentence about why THIS company specifically.

## 14. ATS Optimization (2026 Landscape)

### How ATS Actually Works
Most ATS (Greenhouse, Lever, Workday, iCIMS) are keyword matchers, not AI. They extract
text from your resume, match it against the job description, and score based on keyword
overlap. ~30% of companies now add AI pre-screening on top (HireVue, Pymetrics, custom
LLM filters), but the keyword layer still comes first. Pass that or no human sees the resume.

### ATS-Safe Section Headers
Use these exact names. ATS parsers look for standard headers to categorize content.
Non-standard headers (like "AI/LLM PROJECTS" or "CORE TECHNICAL SKILLS") may cause
the section to be miscategorized or skipped entirely.

**Preferred headers (highest parse rate):**
- SUMMARY or PROFESSIONAL SUMMARY
- TECHNICAL SKILLS
- PROFESSIONAL EXPERIENCE
- EDUCATION
- KEY PROJECTS
- KEY ACHIEVEMENTS
- CERTIFICATIONS

**Also recognized by most ATS:**
- SKILLS, CORE COMPETENCIES
- WORK EXPERIENCE, EXPERIENCE
- ACHIEVEMENTS, NOTABLE PROJECTS
- ADDITIONAL INFORMATION

**Never use:** Role-specific prefixed headers like "KEY PYTHON/ML PROJECTS" or
"CORE TECHNICAL SKILLS" - these fail both ATS parsing and the PDF generator.

### Keyword Placement Strategy
ATS counts keyword frequency, not just presence. For maximum scoring:
1. Put the skill in TECHNICAL SKILLS (gets parsed as a "skill" data field)
2. Use the same skill in at least one PROFESSIONAL EXPERIENCE bullet (proves usage)
3. If applicable, mention it in a KEY PROJECTS bullet (shows depth)

Use the job description's exact phrasing: "Node.js" not "NodeJS", "REST APIs" not
"RESTful services", "React" not "React.js" - unless the JD uses the variant.

### Format Requirements
- **Single column only** - multi-column layouts cause text extraction to interleave columns
- **No graphics, tables, icons, or text boxes** - ATS can't extract text from these
- **Standard fonts** (Arial, Calibri, Helvetica) at 10-12pt
- **No headers/footers** - many ATS skip header/footer regions entirely
- **2 pages maximum** - some ATS truncate after page 2
- **Reverse chronological order** - ATS expects most recent role first

### File Format
- **PDF** works with most modern ATS (Greenhouse, Lever, Ashby, Workday)
- **DOCX** has the highest universal compatibility, especially older ATS (Taleo,
  SuccessFactors, some Fortune 500 custom systems). `python create_pdf.py "Resume.txt" --docx`
  writes both.
- When in doubt, submit PDF. If the application form specifically requests .doc/.docx,
  use that format instead.
- Never submit .txt, .rtf, or .pages

### Ampersands and Special Characters
- Avoid `&` in .txt resume files - use "and" instead (e.g., "R and D Engineer")
- The PDF generator escapes `&` automatically, but ATS text extraction may not
- Other safe characters: pipes `|`, bullets, dashes, parentheses, forward slashes

### What NOT to Do
- No invisible/hidden text, white-on-white text, or keyword stuffing - ATS like
  ManpowerGroup flag ~10% of scanned resumes for hidden text manipulation. This can
  result in permanent blacklisting, not just rejection.
- No "References available upon request" - wastes space and is assumed
- Don't repeat the entire job description in tiny text - modern ATS detect this
- Don't use acronyms without also spelling them out once (ATS may search for either)
