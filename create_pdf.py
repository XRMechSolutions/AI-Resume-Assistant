import os
import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def parse_resume_txt(file_path):
    """Parse a resume text file and extract sections."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    current_section = None
    current_content = []
    
    lines = content.split('\n')
    
    # Extract header info (name, title, contact) - look for contact info patterns
    header_lines = []
    i = 0
    header_complete = False
    
    while i < len(lines) and not header_complete:
        line = lines[i].strip()
        
        # Check if we've hit a major section header
        if line and any(line.upper() == pattern for pattern in ['PROFESSIONAL SUMMARY', 'SUMMARY', 'OBJECTIVE', 'TECHNICAL SKILLS', 'SKILLS']):
            header_complete = True
            break
        
        # Add non-empty lines to header until we hit a section
        if line:
            header_lines.append(line)
        elif header_lines and len(header_lines) >= 2:  # Empty line after we have at least name and one contact line
            header_complete = True
            break
        
        i += 1
    
    sections['header'] = header_lines
    
    # Common section headers to look for
    section_patterns = [
        'SUMMARY', 'PROFESSIONAL SUMMARY', 'OBJECTIVE',
        'TECHNICAL SKILLS', 'SKILLS', 'CORE COMPETENCIES', 'CORE TECHNICAL CAPABILITIES',
        'PROFESSIONAL EXPERIENCE', 'WORK EXPERIENCE', 'EXPERIENCE',
        'EDUCATION',
        'NOTABLE PROJECTS', 'KEY PROJECTS', 'PROJECTS',
        'KEY ACHIEVEMENTS', 'ACHIEVEMENTS',
        'CERTIFICATIONS', 'CERTIFICATIONS & TRAINING',
        'ADDITIONAL INFORMATION', 'PERSONAL INTERESTS'
    ]
    
    # Process the rest of the file from where header ended
    for line_idx in range(i, len(lines)):
        line = lines[line_idx].rstrip()
        
        # Check if this line is a section header
        is_section = False
        for pattern in section_patterns:
            if line.upper().strip() == pattern or line.upper().strip().endswith(pattern):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                # Start new section
                current_section = pattern.replace(' ', '_').upper()
                current_content = []
                is_section = True
                break
        
        if not is_section:
            if current_section or line.strip():  # Add to current section or capture orphaned content
                current_content.append(line)
    
    # Save the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def create_resume_pdf(txt_file_path, output_pdf_path=None):
    """Create a PDF from a resume text file."""
    
    if not os.path.exists(txt_file_path):
        print(f"Error: File {txt_file_path} not found!")
        return
    
    # Parse the resume
    sections = parse_resume_txt(txt_file_path)
    
    # Determine output filename
    if output_pdf_path is None:
        base_name = os.path.splitext(txt_file_path)[0]
        output_pdf_path = base_name + ".pdf"
    
    # Create the PDF
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter,
                            rightMargin=0.5*inch, leftMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Define custom styles
    name_style = ParagraphStyle(
        'CustomName',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=2,
        alignment=TA_CENTER,
        leading=18
    )
    
    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#444444'),
        spaceAfter=2,
        alignment=TA_CENTER,
        leading=12
    )
    
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor('#000080'),
        spaceAfter=6,
        spaceBefore=10,
        leading=13,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=15,
        spaceAfter=2,
        alignment=TA_LEFT
    )
    
    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontSize=10.5,
        textColor=colors.HexColor('#000000'),
        spaceAfter=3,
        spaceBefore=6,
        leading=12,
        fontName='Helvetica-Bold'
    )
    
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=2,
        leading=12
    )
    
    # Process header
    if 'header' in sections and sections['header']:
        header_lines = sections['header']
        
        # First line is usually the name - bold the entire name
        if header_lines:
            name = f"<b>{header_lines[0]}</b>"
            elements.append(Paragraph(name, name_style))
        
        # Rest are contact details
        for line in header_lines[1:]:
            if line:
                # Make links clickable
                line = re.sub(r'(github\.com/\S+)', r'<link href="https://\1">\1</link>', line)
                line = re.sub(r'(linkedin\.com/\S+)', r'<link href="https://\1">\1</link>', line)
                line = re.sub(r'(\S+@\S+\.\S+)', r'<link href="mailto:\1">\1</link>', line)
                elements.append(Paragraph(line, contact_style))
        
        elements.append(Spacer(1, 12))
    
    # Process sections in a logical order
    section_order = [
        'SUMMARY', 'PROFESSIONAL_SUMMARY',
        'TECHNICAL_SKILLS', 'SKILLS', 'CORE_COMPETENCIES', 'CORE_TECHNICAL_CAPABILITIES',
        'PROFESSIONAL_EXPERIENCE', 'WORK_EXPERIENCE', 'EXPERIENCE',
        'NOTABLE_PROJECTS', 'KEY_PROJECTS', 'PROJECTS',
        'EDUCATION',
        'KEY_ACHIEVEMENTS', 'ACHIEVEMENTS',
        'CERTIFICATIONS', 'CERTIFICATIONS_&_TRAINING',
        'ADDITIONAL_INFORMATION', 'PERSONAL_INTERESTS'
    ]
    
    for section_key in section_order:
        if section_key in sections and sections[section_key]:
            content = sections[section_key]
            
            # Add section heading
            section_title = section_key.replace('_', ' ')
            elements.append(Paragraph(f"<b>{section_title}</b>", section_style))
            
            # Process content based on section type
            if section_key in ['PROFESSIONAL_EXPERIENCE', 'WORK_EXPERIENCE', 'EXPERIENCE']:
                # Parse job entries
                process_experience_section(content, elements, job_title_style, company_style, bullet_style)
            
            elif section_key in ['TECHNICAL_SKILLS', 'SKILLS', 'CORE_COMPETENCIES', 'CORE_TECHNICAL_CAPABILITIES']:
                # Parse skills section
                process_skills_section(content, elements, bullet_style, normal_style)
            
            elif section_key in ['NOTABLE_PROJECTS', 'KEY_PROJECTS', 'PROJECTS']:
                # Parse projects
                process_projects_section(content, elements, job_title_style, bullet_style)
            
            elif section_key in ['EDUCATION']:
                # Parse education
                process_education_section(content, elements, normal_style, bullet_style)
            
            elif section_key in ['KEY_ACHIEVEMENTS', 'ACHIEVEMENTS', 'CERTIFICATIONS', 'CERTIFICATIONS_&_TRAINING']:
                # Parse as bullet points
                process_bullet_section(content, elements, bullet_style)
            
            else:
                # Default: treat as paragraph or multi-line content
                paragraphs = content.split('\n\n')  # Split by double newline for paragraphs
                for para in paragraphs:
                    para = para.strip()
                    if para:
                        # Join lines within a paragraph with spaces
                        para_text = ' '.join(line.strip() for line in para.split('\n') if line.strip())
                        if para_text:
                            elements.append(Paragraph(para_text, normal_style))
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"[SUCCESS] Resume PDF created: {output_pdf_path}")
        return output_pdf_path
    except Exception as e:
        print(f"[ERROR] Error creating PDF: {e}")
        return None

def process_experience_section(content, elements, job_style, company_style, bullet_style):
    """Process professional experience section."""
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for job titles (usually contain | or dates like "2023 - Present")
        if '|' in line or re.search(r'\d{4}\s*[-–]\s*(Present|\d{4})', line):
            # This looks like a job header
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    title_company = parts[0].strip()
                    dates = parts[1].strip() if len(parts) > 1 else ''
                    
                    # Create job header with dates aligned right
                    job_text = f"<b>{title_company}</b>"
                    if dates:
                        job_text += f"  <i>({dates})</i>"
                    elements.append(Paragraph(job_text, job_style))
            else:
                elements.append(Paragraph(f"<b>{line}</b>", job_style))
            
            i += 1
            
            # Check for location line (e.g., "Remote", "Seattle, WA")
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line and not next_line.startswith('•') and not ':' in next_line and len(next_line.split()) <= 3:
                    # Likely a location line
                    elements.append(Paragraph(f"<i>{next_line}</i>", company_style))
                    i += 1
            
            # Collect content for this job
            while i < len(lines):
                line = lines[i].strip()
                
                if not line:
                    i += 1
                    continue
                    
                # Check if this is the next job entry
                if '|' in line and re.search(r'\d{4}', line):
                    break
                    
                # Check for sub-sections like "Key Unity Projects:"
                if line.endswith(':') and not line.startswith('•'):
                    elements.append(Paragraph(f"<b>{line}</b>", company_style))
                    i += 1
                    
                    # Process items under this sub-section
                    while i < len(lines):
                        sub_line = lines[i].strip()
                        if not sub_line:
                            i += 1
                            break
                        if sub_line.startswith('-'):
                            # Sub-bullet with dash
                            elements.append(Paragraph('  ' + sub_line, bullet_style))
                        elif '|' in sub_line and re.search(r'\d{4}', sub_line):
                            # Next job, don't consume
                            break
                        elif sub_line.endswith(':') and not sub_line.startswith('•'):
                            # Another sub-section, don't consume
                            break
                        elif sub_line.startswith('•'):
                            # Regular bullet, end of sub-section
                            break
                        else:
                            # Part of sub-section
                            elements.append(Paragraph('  - ' + sub_line, bullet_style))
                        i += 1
                    continue
                    
                # Regular bullet points
                if line.startswith('•'):
                    elements.append(Paragraph(line, bullet_style))
                elif line and line[0].isupper() and ':' not in line:
                    # Likely a new section or standalone line
                    if re.search(r'\d{4}', line):
                        # Might be next job
                        break
                    else:
                        # Add as bullet
                        elements.append(Paragraph('• ' + line, bullet_style))
                i += 1
        else:
            i += 1

def process_skills_section(content, elements, bullet_style, normal_style):
    """Process skills section."""
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a categorized skill (has a colon)
        if ':' in line and not line.startswith('•'):
            # Bold the category
            parts = line.split(':', 1)
            formatted = f"<b>{parts[0]}:</b>{parts[1]}"
            if not line.startswith('•'):
                formatted = '• ' + formatted
            elements.append(Paragraph(formatted, bullet_style))
        elif line.startswith('•'):
            # Already a bullet point
            if ':' in line:
                parts = line.split(':', 1)
                formatted = f"{parts[0].replace('•', '• <b>')}:</b>{parts[1]}"
                elements.append(Paragraph(formatted, bullet_style))
            else:
                elements.append(Paragraph(line, bullet_style))
        else:
            # Make it a bullet point
            elements.append(Paragraph('• ' + line, bullet_style))

def process_projects_section(content, elements, project_style, bullet_style):
    """Process projects section."""
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Check if this looks like a project title (with year or not starting with bullet)
        if not line.startswith('•') and (re.search(r'\(\d{4}\)', line) or 
                                         (line[0].isupper() and not line.startswith('-'))):
            # This is a project title
            elements.append(Paragraph(f"<b>{line}</b>", project_style))
            i += 1
            
            # Collect project description bullets
            while i < len(lines):
                desc_line = lines[i].strip()
                if not desc_line:
                    i += 1
                    break
                    
                # Check if this is a new project title
                if not desc_line.startswith('•') and not desc_line.startswith('-') and \
                   (re.search(r'\(\d{4}\)', desc_line) or 
                    (desc_line[0].isupper() and len(desc_line.split()) > 1)):
                    # Next project, don't consume
                    break
                    
                if desc_line.startswith('•'):
                    elements.append(Paragraph(desc_line, bullet_style))
                else:
                    # Add as bullet if not already
                    elements.append(Paragraph('• ' + desc_line, bullet_style))
                i += 1
        elif line.startswith('•'):
            elements.append(Paragraph(line, bullet_style))
            i += 1
        else:
            # Standalone line, treat as bullet
            elements.append(Paragraph('• ' + line, bullet_style))
            i += 1

def process_education_section(content, elements, normal_style, bullet_style):
    """Process education section."""
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Education entries usually have degree type or school name
        if 'Master' in line or 'Bachelor' in line or 'University' in line or 'School' in line:
            # Bold degree names
            line = re.sub(r'(Master[^,\-|]*)', r'<b>\1</b>', line)
            line = re.sub(r'(Bachelor[^,\-|]*)', r'<b>\1</b>', line)
            elements.append(Paragraph(line, normal_style))
        elif line.startswith('•'):
            elements.append(Paragraph(line, bullet_style))
        else:
            elements.append(Paragraph(line, normal_style))

def process_bullet_section(content, elements, bullet_style):
    """Process sections that are primarily bullet points."""
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if not line.startswith('•'):
            line = '• ' + line
        
        # Bold important keywords
        line = re.sub(r'(Patent:)', r'<b>\1</b>', line)
        line = re.sub(r'(Award:)', r'<b>\1</b>', line)
        line = re.sub(r'(Published:)', r'<b>\1</b>', line)
        
        elements.append(Paragraph(line, bullet_style))

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        # Process specific file
        txt_file = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
        create_resume_pdf(txt_file, output_pdf)
    else:
        # Process all .txt resume files in the current directory
        # Look for files containing "Resume" in the name
        import glob
        resume_files = glob.glob('*Resume*.txt')

        if not resume_files:
            print("No resume .txt files found in current directory.")
            print("Usage: python create_pdf.py [resume_file.txt] [output.pdf]")
            return

        for txt_file in resume_files:
            print(f"\nProcessing {txt_file}...")
            create_resume_pdf(txt_file)

if __name__ == "__main__":
    main()