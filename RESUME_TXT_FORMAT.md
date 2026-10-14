# Resume .txt Format Reference

This file documents the exact format rules that create_pdf.py expects.
Deviating from these rules causes broken PDF output.

---

## Section Headers

Must be EXACT matches (all caps) from this list:

```
SUMMARY
TECHNICAL SKILLS
PROFESSIONAL EXPERIENCE
EDUCATION
KEY PROJECTS
KEY ACHIEVEMENTS
```

Other recognized variants: PROFESSIONAL SUMMARY, SKILLS, CORE COMPETENCIES,
WORK EXPERIENCE, EXPERIENCE, NOTABLE PROJECTS, PROJECTS, ACHIEVEMENTS,
CERTIFICATIONS, ADDITIONAL INFORMATION

**Spanish-language resumes** can use these headers instead. They render in
Spanish and are parsed as the matching English section: PERFIL PROFESIONAL or RESUMEN (Summary),
COMPETENCIAS TÉCNICAS or HABILIDADES TÉCNICAS (Technical Skills), EXPERIENCIA PROFESIONAL,
FORMACIÓN or FORMACIÓN ACADÉMICA (Education), PROYECTOS DESTACADOS, LOGROS DESTACADOS, IDIOMAS
(one line, shown as plain text). Job dates may use Spanish months (`Ene`, `Abr`, `Ago`, `Dic`) and
`Actualidad`, e.g. `Ago 2023 - Actualidad`. Degree lines starting `Máster en` or `Grado en` are bolded.

**Do NOT use:** KEY BACKEND PROJECTS, KEY PYTHON/ML PROJECTS, or any other
variant not in the list above - the section will be silently skipped.

---

## Header Block (Name / Contact)

```
YOUR NAME
Job Title | Specialization | Other
email | phone | location
GitHub: github.com/yourname | LinkedIn: www.linkedin.com/in/yourname
[blank line]
```

- GitHub and LinkedIn URLs are made clickable automatically
- Email is made clickable automatically
- Blank line ends the header block
- The first line (your name) is used for the PDF/DOCX title and author metadata

---

## Job Entry Format

```
Company Name | Job Title                                    Mon YYYY - Mon YYYY
Location
```

Rules:
- **One pipe only** between company and title - everything after goes on one line
- Date must be in format `Mon YYYY - Mon YYYY` or `Mon YYYY - Present`
  (e.g., `Aug 2023 - Present`, `May 2021 - Sep 2023`)
- Location line must be **3 words or fewer** - "Remote", "Remote (EU)",
  "Seattle, WA", "Golden, CO" all work. More than 3 words breaks detection.
- Avoid `&` anywhere in the .txt file - use "and" instead (e.g., "R and D" not "R&D").
  The PDF generator has an `_esc()` function that converts `&` to `&amp;` for ReportLab,
  but spelling out "and" is safer for both PDF rendering and ATS text extraction.

**Sub-roles within a job** (several titles at one employer) use the format:
```
Role Name (YYYY-YYYY)
```
These get detected as bold headings because they contain a year range.

---

## Bullet Points

**Critical rule: one bullet = one line. No exceptions.**

The PDF handles word wrapping. The .txt does not need to wrap manually.

```
• This is a bullet point that can be as long as it needs to be without any manual line breaks
• Next bullet point
```

**Wrong:**
```
• This bullet was manually wrapped because it looked too long
  in the text editor and now the second line becomes its own bullet
```

Continuation lines that start with a capital letter become new bullets.
Continuation lines that start lowercase are silently dropped.
Both are bugs. Use single lines.

---

## Skills Section

```
TECHNICAL SKILLS
Category: skill1, skill2, skill3
Category: skill1, skill2
```

- Category labels get bolded automatically
- No bullets needed - the parser adds them
- One category per line

---

## Projects Section

```
KEY PROJECTS

Project Name (YYYY)
• Bullet describing the project
• Another bullet

Next Project (YYYY)
• Bullet
```

- Project title must not start with `•`
- Description must use `•` bullets - plain text lines get treated as new project titles

---

## Education Section

```
EDUCATION
Master of Science, Field - School Name
Bachelor of Science, Field - School Name
```

- No dates (omit graduation years)
- Degree type gets bolded automatically

---

## Sub-section Headings Inside a Job

A line ending in `:` (not starting with `•`) becomes a bold sub-heading, and the `- ` lines under it
render as indented items. Use it to group client work under a consulting role:

```
Client projects:
- Client A: what you built
- Client B: what you built
```

---

## Generating

```
python create_pdf.py "Resume.txt" ["out.pdf"] [--docx] [--verbose]
```

- `--docx` also writes a Word copy (for application forms that require .doc/.docx)
- `--verbose` lists every parsed section and its line count; use it when a section seems to be missing
- An ALL-CAPS line that is not a known header prints `[WARN] Possible unrecognized section header`
- With no file argument, every `*Resume*.txt` in the current folder is rendered
- Check the page count afterwards (2 pages maximum)

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Multi-line bullet | Each line becomes a bullet | One line per bullet |
| Location > 3 words | Location becomes a bullet | Shorten to ≤3 words |
| `&` anywhere in text | May mangle in PDF or ATS | Spell out "and" |
| Wrong section header name | Section skipped entirely | Use exact names from list above |
| Blank line inside bullet block | Ends the bullet group | Keep bullets contiguous |
