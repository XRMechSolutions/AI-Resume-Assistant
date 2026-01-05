# AI Resume Assistant

An AI-powered resume customization system using Claude Code. This system helps you:

- **Customize resumes** for specific job applications without fabricating experience
- **Search job boards** and evaluate opportunities based on your skills
- **Track applications** and follow-ups
- **Generate professional PDFs** from plain text resumes

## How It Works

The core of this system is `CLAUDE.md` - a comprehensive instruction file that teaches Claude Code how to:

1. **Write in your voice** based on your verified experience
2. **Never fabricate** skills, metrics, or experience you don't have
3. **Tailor resumes** to match job descriptions using only verified information
4. **Evaluate jobs** against your actual skills and constraints
5. **Track your job search** across multiple applications

## Quick Start

### 1. Clone and Setup

```bash
git clone [this-repo]
cd ai-resume-assistant
```

### 2. Create Your Personal Files

Copy the templates to create your personal versions:

```bash
# Copy the main instruction file
cp CLAUDE.template.md CLAUDE.md

# Copy example files
cp examples/Example_Source_of_Truth.md YourName_Source_of_Truth.md
cp examples/Example_Anti_Fabrication_Checklist.md ANTI_FABRICATION_CHECKLIST.md
cp examples/Job_Application_Tracker_Template.csv Job_Application_Tracker.csv
cp examples/Job_Search_Queue_Template.csv Job_Search_Queue.csv
```

### 3. Fill In Your Information

Edit these files with your personal information:

1. **`CLAUDE.md`** - Replace all `{{PLACEHOLDER}}` values with your info
2. **`YourName_Source_of_Truth.md`** - Your complete verified experience
3. **`ANTI_FABRICATION_CHECKLIST.md`** - Technologies you do/don't know

### 4. Install PDF Dependencies

```bash
pip install reportlab
```

### 5. Start Using

Open Claude Code in this directory and start customizing resumes:

```
> Here's a job description for a Senior Backend Developer at TechCorp...
```

Claude will read your source of truth, verify every claim, and create a tailored resume.

## File Structure

```
ai-resume-assistant/
├── CLAUDE.template.md          # Shareable workflow logic (tracked in git)
├── CLAUDE.md                   # Your personal version (git-ignored)
├── create_pdf.py               # PDF generation script
├── Job_Boards.csv              # Public job board list
├── README.md                   # This file
├── .gitignore                  # Excludes personal files
│
├── examples/                   # Templates for new users
│   ├── Example_Source_of_Truth.md
│   ├── Example_Anti_Fabrication_Checklist.md
│   ├── Job_Application_Tracker_Template.csv
│   └── Job_Search_Queue_Template.csv
│
├── [Personal - git-ignored]/
│   ├── YourName_Source_of_Truth.md
│   ├── ANTI_FABRICATION_CHECKLIST.md
│   ├── Job_Application_Tracker.csv
│   ├── Job_Search_Queue.csv
│   ├── *Resume*.txt / .pdf
│   ├── *CoverLetter*.txt
│   ├── JobSearches/            # Per-company application folders
│   └── Archive/                # Past applications
```

## Contributing Improvements

When you improve the workflow logic and want to share it:

### Workflow for Contributing Changes

1. **Make your improvement** in your personal `CLAUDE.md`
2. **Test it** to make sure it works
3. **Extract the logic** (not personal data) to `CLAUDE.template.md`
4. **Commit and push** `CLAUDE.template.md`

### What to Contribute

**DO share:**
- New workflow sections (e.g., better job evaluation criteria)
- Improved anti-fabrication rules
- Better resume best practices
- New job search strategies
- Bug fixes in the process

**DON'T share:**
- Your personal contact info
- Your specific skills/experience
- Your job application history
- Your source of truth content

### Example: Adding a New Feature

Say you create a great new "Interview Prep" workflow:

1. Add it to your `CLAUDE.md` and test it
2. Copy the section to `CLAUDE.template.md`, replacing any personal references with `{{PLACEHOLDER}}` syntax
3. Commit: `git add CLAUDE.template.md && git commit -m "Add interview prep workflow"`

## Key Concepts

### Source of Truth

Your `*_Source_of_Truth.md` file is the single source of verified information. The AI will ONLY use information from this file when creating resumes. This prevents:

- Fabricated skills
- Made-up metrics
- Assumed experience
- Inflated achievements

### Anti-Fabrication Checklist

The checklist reminds Claude what you DO and DON'T know. It's a safety net that gets read before every resume task.

### Job Evaluation Tiers

Jobs are scored and categorized into tiers:
- **Tier 1**: Perfect fit (80%+ match) - Apply immediately
- **Tier 2**: Strong match (60-80%) - Worth customizing
- **Tier 3**: Transferable (40-60%) - Apply if time permits
- **Skip**: Below 40% or has disqualifiers

## Usage Examples

### Customize a Resume

```
> Here's a job posting for Senior Full Stack Developer at Acme Corp:
> [paste job description]
>
> Please create a tailored resume.
```

### Search for Jobs

```
> Check for jobs
```

### Evaluate Multiple Opportunities

```
> Here are 5 job postings I found. Rank them by fit:
> [paste job descriptions]
```

### Track an Application

```
> I applied to Acme Corp for the Senior Full Stack role
```

## PDF Generation

Create professional PDFs from text resumes:

```bash
# Single file
python create_pdf.py "Your_Resume.txt"

# All resumes in directory
python create_pdf.py
```

## Tips for Best Results

1. **Be thorough in your Source of Truth** - The more detail you provide, the better Claude can tailor resumes

2. **Update regularly** - Add new projects and skills as you gain them

3. **Be honest about skill levels** - Mark things as "familiar" vs "expert" appropriately

4. **Include specific numbers** - Metrics from your actual experience are gold

5. **List what you DON'T know** - Prevents accidental fabrication

## License

MIT - Feel free to use, modify, and share.
