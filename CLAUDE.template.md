# CLAUDE.md - AI Resume Assistant Template

This file provides guidance to Claude Code (claude.ai/code) when working with resumes in this repository.

**SETUP INSTRUCTIONS**: Copy this file to `CLAUDE.md` and replace all `{{PLACEHOLDER}}` values with your personal information. Then create your source of truth document following the template in `examples/`.

---

## RESUME CREATION WORKFLOW - ALWAYS FOLLOW THIS ORDER

When user provides a job description for resume customization:

1. **FIRST**: Read all mandatory documents (see MANDATORY FIRST STEP below)
2. **SECOND**: Create the resume following the guidelines
3. **THIRD**: Generate PDF using create_pdf.py
4. **NEVER**: Skip reading the guideline documents or create resumes from memory

## CRITICAL: ANTI-FABRICATION RULES

### MANDATORY FIRST STEP FOR ANY RESUME TASK
**ALWAYS read these documents IN THIS ORDER before ANY resume customization:**
```bash
# Step 1: Read the anti-fabrication rules
Read "{{PATH_TO_RESUMES}}/ANTI_FABRICATION_CHECKLIST.md"

# Step 2: Read the source of truth document
Read "{{PATH_TO_RESUMES}}/{{YOUR_NAME}}_Source_of_Truth.md"
```

**DO NOT PROCEED WITHOUT READING THESE DOCUMENTS FIRST**

### GOLDEN RULE
**If it's not in the source documents, DO NOT add it to the resume.**
- No similar technologies (e.g., Vue.js when they know React)
- No made-up metrics (performance improvements, cost savings)
- No assumed experience (e.g., Unreal because they know Unity)

### VERIFICATION PROCESS
For each job requirement:
1. Search in source documents
2. If found -> Use exact wording
3. If not found -> DO NOT ADD
4. If uncertain -> ASK USER

---

## QUICK REFERENCE: {{YOUR_NAME}} Core Skills & Experience

### Contact & Status
- **Email**: {{YOUR_EMAIL}}
- **Phone**: {{YOUR_PHONE}}
- **GitHub**: {{YOUR_GITHUB}}
- **LinkedIn**: {{YOUR_LINKEDIN}}
- **Location**: {{YOUR_LOCATION}}
- **Work Auth**: {{YOUR_WORK_AUTHORIZATION}}
- **Remote Preference**: {{REMOTE_PREFERENCE}}

### Current Role ({{CURRENT_START_DATE}} - Present)
**{{CURRENT_COMPANY}}** - {{CURRENT_TITLE}}
- **Active Projects**:
  - {{PROJECT_1}}
  - {{PROJECT_2}}
  - {{PROJECT_3}}

### Core Technical Skills (VERIFIED)
<!-- Copy your verified skills from your Source of Truth document -->

#### Programming Languages
- **Primary**: {{PRIMARY_LANGUAGES}}
- **Secondary**: {{SECONDARY_LANGUAGES}}

#### Frameworks & Platforms
- {{FRAMEWORK_CATEGORY_1}}: {{TOOLS}}
- {{FRAMEWORK_CATEGORY_2}}: {{TOOLS}}

#### Cloud & Infrastructure
- {{CLOUD_PLATFORMS}}
- {{INFRASTRUCTURE_TOOLS}}

### Key Career Highlights
<!-- Summarize your major roles and achievements -->

#### {{PREVIOUS_COMPANY_1}} ({{YEARS}})
- {{KEY_ACHIEVEMENT_1}}
- {{KEY_ACHIEVEMENT_2}}

#### {{PREVIOUS_COMPANY_2}} ({{YEARS}})
- {{KEY_ACHIEVEMENT_1}}
- {{KEY_ACHIEVEMENT_2}}

### Notable Achievements
- {{ACHIEVEMENT_1}}
- {{ACHIEVEMENT_2}}
- {{ACHIEVEMENT_3}}

### Education
- {{DEGREE_1}} - {{SCHOOL_1}}
- {{DEGREE_2}} - {{SCHOOL_2}}

### Certifications (ACTUAL - only list what you have)
- {{CERTIFICATION_1}}
- {{CERTIFICATION_2}}
- **NO** {{CERTIFICATION_YOU_DONT_HAVE}} (have experience only)

### DO NOT CLAIM - ABSOLUTE PROHIBITIONS
<!-- List technologies and experiences you should NEVER claim -->
- {{TECHNOLOGY_YOU_DONT_KNOW_1}}
- {{TECHNOLOGY_YOU_DONT_KNOW_2}}
- {{EXPERIENCE_YOU_DONT_HAVE}}
- Any statistics not explicitly documented in source files
- Team size numbers unless specified
- Budget amounts unless documented
- Performance improvements unless exact numbers given

---

## Project Purpose
This repository manages customized resumes and cover letters for specific job applications. The goal is to tailor application materials to specific positions while maintaining authentic voice and verified experience.

## Repository Structure

### Main Directory
- **Base Resume Files**: Core resume templates in .txt format (generate PDFs using create_pdf.py)
- **Cover Letter Templates**: General and company-specific cover letters
- **Supporting Documents**: Source of truth, anti-fabrication checklist

### JobSearches/
Subfolder structure for organizing application materials by company/position. Each subfolder contains:
- Job description (.txt file)
- Customized resume for that specific position
- Customized cover letter when applicable

### Archive/
Historical versions of resumes and cover letters from previous applications.

## Customization Workflow

When customizing for a new position:

0. **MANDATORY**: Read source documents first (see anti-fabrication rules above)

1. **CHECK TRACKER FIRST**: Read `Job_Application_Tracker.csv` to verify this company/position hasn't already been applied to

2. **Create New Job Subfolder**: Create a new folder under `JobSearches/[CompanyName]/`

3. **Save Job Description**: Save the job posting as a .txt file in the subfolder

4. **Select Base Template**: Choose the most appropriate base resume template

5. **Customize Content**:
   - Match technical skills ONLY if verified in source documents
   - Use exact project names from source of truth
   - Include only documented metrics and achievements
   - Maintain consistent tone and voice throughout

6. **Cover Letter Creation**: If needed, customize to:
   - Address specific requirements from the job posting
   - Connect experience directly to company needs
   - Maintain professional yet personable tone

7. **UPDATE TRACKER**: After applying, add entry to `Job_Application_Tracker.csv`

---

## Resume Best Practices for Software Development

### Age-Conscious Presentation (40+ Developers)
- **Focus on recent 10-15 years** - Older experience can be summarized briefly or omitted
- **Emphasize current tech stack** - Lead with modern technologies
- **Show continuous learning** - Highlight recent projects with cutting-edge tech
- **Avoid graduation years** unless recent or specifically requested
- **Use "10+ years" or "extensive experience"** rather than exact years that reveal age

### Strategic Information Management

#### What to Emphasize:
- **Production systems currently in use** - Shows active, relevant experience
- **Remote work success** - Highly valued post-2020
- **Cross-functional capabilities** - Shows versatility
- **AI/ML integration** - Currently the hottest area in tech
- **Patents/Publications** - Demonstrates innovation and expertise
- **Open source contributions** - Shows passion and current activity

#### What to Downplay or Omit:
- **Dates before 2010** unless directly relevant
- **Outdated technologies** unless job specifically requires them
- **Non-technical roles** from early career
- **Education dates** if degree is 15+ years old
- **References to "decades of experience"** - Use "extensive" instead

### Truth vs. Strategic Presentation

#### Acceptable Enhancements:
- **Aggregating similar experiences** - "Developed backend services" covers many small projects
- **Using industry-standard terms** - "Microservices" for modular backend design
- **Highlighting transferable skills** - Similar platform experience applies
- **Emphasizing impact** - Focus on what you achieved, not just what you did

#### Never Do:
- **Claim certifications you don't have**
- **List technologies you've never used**
- **Inflate job titles** significantly
- **Create fictional projects or companies**
- **Claim sole credit for team achievements**
- **Add years to experience duration**

### ATS (Applicant Tracking System) Optimization
- **Match keywords exactly** from job description when truthful
- **Use standard section headers** (Professional Experience, not "My Journey")
- **Include technologies in multiple contexts** - Skills section AND experience bullets
- **Avoid graphics, tables, or columns** in initial applications
- **Save as .txt first** to verify ATS readability

### Length and Formatting Rules
- **2 pages maximum** for most positions (1 page for <5 years experience)
- **No "References available upon request"** - Assumed and wastes space
- **No objective statements** - Use professional summary instead
- **Consistent formatting** - Same bullet style, font, spacing throughout
- **Reverse chronological order** - Most recent first, always

---

## Standing Out in an AI-Saturated Application Pool

### The AI Resume Arms Race Problem
Most applicants now use AI to optimize resumes, creating a sea of similar-looking, keyword-stuffed applications. To stand out:

### Differentiation Strategies

#### 1. Specific Project Details Others Can't Fake
- Name actual products you've built
- Include verifiable achievements (awards, patents, publications)
- Reference specific technologies in context
- These show problem-solving that can't be faked

#### 2. Unique Technology Combinations
Highlight unusual skill combinations that are hard to fake and rare in the market.

#### 3. Quantifiable But Unusual Metrics
Avoid generic percentages. Use specific, memorable numbers from your actual experience.

#### 4. The "Proof of Work" Approach
Include details that prove hands-on experience - specific technical challenges you solved, workarounds you created, etc.

#### 5. Strategic Imperfection
Perfect AI-generated resumes look suspicious. Include:
- One or two technologies you're "familiar with" not "expert in"
- Shows honesty and self-awareness

#### 6. The Story Arc
Create a narrative that AI typically misses - show intentional career progression and adaptability.

### Per-Application Customization Rules

#### Phase 1: Initial Parsing
1. Extract EXACT job title and use it in your summary
2. Identify the 3-5 most emphasized skills (usually repeated)
3. Note any unusual requirements (specific frameworks, domains)

#### Phase 2: Strategic Matching
1. **Exact Keyword Match**: Use their EXACT phrasing when truthful
2. **Project Selection**: Choose 2-3 projects that best match
3. **Skills Reordering**: List their requirements first in skills section

#### Phase 3: The "Extra Mile" Details
- Research the company's actual products and reference similar work
- Mention their specific industry challenges you've solved
- Include a relevant side project that aligns with their mission

### The Ultimate Test
Before sending, ask:
1. Could any other applicant have written this EXACT resume?
2. Does it contain specific details only you would know?
3. Does it tell a coherent story, not just list skills?
4. Would a human reader remember something specific about it?

---

## Job Opportunity Quick Evaluation Guide

### When User Provides Multiple Job Listings to Evaluate

Use this framework to quickly assess and prioritize opportunities:

#### TIER 1: PERFECT FIT (Apply Immediately)
Jobs matching 80%+ of criteria:
- **Remote-first** or matches your location preference
- **Tech match**: Your primary skills
- **Recent skills**: Technologies you're currently using
- **Domain match**: Industries you have experience in
- **No blockers**: No clearance/visa/location restrictions that apply to you

#### TIER 2: STRONG MATCH (Worth Customizing)
Jobs with 60-80% match:
- Your secondary skills are primary requirements
- Similar but not exact technology match
- Industry you could transfer into

#### TIER 3: TRANSFERABLE (Apply if Time Permits)
Jobs with 40-60% match:
- General software engineering roles
- Your skills are "nice to have" not required
- Would require emphasizing transferable experience

#### AUTOMATIC DISQUALIFIERS (Skip These)
Configure based on your constraints:
- {{YOUR_DISQUALIFIER_1}} (e.g., On-site only)
- {{YOUR_DISQUALIFIER_2}} (e.g., Security clearance required)
- {{YOUR_DISQUALIFIER_3}} (e.g., Technology you don't know)

### Quick Scoring Matrix

**Technical Fit (0-5 points each)**:
- Languages match: ___
- Platform/framework match: ___
- Domain experience: ___
- Modern tech alignment: ___

**Practical Fit (0-10 points each)**:
- Remote work allowed: ___
- No blockers (clearance/visa): ___
- Timezone compatibility: ___

**Score Interpretation**:
- 50+ points: APPLY IMMEDIATELY
- 35-49 points: Customize and apply
- 20-34 points: Generic application if time
- <20 points: Skip

---

## PDF Generation Process

After customizing resumes:

1. **Save resume as .txt file** in the appropriate folder

2. **Generate PDF using create_pdf.py**:
   ```bash
   python create_pdf.py "Your_Resume_Name.txt"
   ```

3. **The script will**:
   - Parse the .txt file structure
   - Apply professional formatting
   - Create clickable links for GitHub, LinkedIn, and email
   - Output a PDF with the same name

---

## Automated Job Search Workflow

### Trigger Phrases
When user says any of these, initiate job search:
- "check for jobs"
- "find new jobs"
- "job search"
- "look for positions"
- "scan job boards"

### Infrastructure Files

**Job_Boards.csv** - List of job boards to check
- Columns: Board Name, URL, Category, Region, Last Checked, Notes

**Job_Search_Queue.csv** - Jobs found pending review
- Columns: Company, Position, URL, Date Found, Source Board, Status, Fit Score, Category, Remote Type, Notes
- Status values: New, Reviewing, Ready to Apply, Applied, Rejected, Saved for Later

**Job_Application_Tracker.csv** - Applied jobs tracking

### Job Search Workflow Steps

#### Phase 1: Discovery
1. Read Job_Boards.csv to get list of sources
2. Check Last Checked dates - prioritize boards not checked recently
3. For each board, search for postings matching your skills
4. Filter results using your automatic disqualifiers
5. Score each job using the Quick Scoring Matrix
6. Add promising jobs to Job_Search_Queue.csv

#### Phase 2: Review
1. Present findings grouped by tier
2. Ask user which jobs to pursue
3. Update status for selected jobs

#### Phase 3: Application Prep
1. Fetch full job description
2. Save to JobSearches/[CompanyName]/
3. Follow standard resume customization workflow
4. Generate PDF

#### Phase 4: Post-Application
1. User confirms application submitted
2. Add entry to Job_Application_Tracker.csv
3. Set follow-up date

### Quick Commands Reference

| User Says | Claude Does |
|-----------|-------------|
| "check for jobs" | Run Discovery + Review |
| "prepare [company] application" | Run Application Prep |
| "I applied to [company]" | Update tracker |
| "add job board [url]" | Add to Job_Boards.csv |
| "show queue" | Display pending jobs |
| "show tracker" | Display application history |

---

## Personal Notes
<!-- Add any personal preferences, constraints, or notes here -->

{{YOUR_PERSONAL_NOTES}}
