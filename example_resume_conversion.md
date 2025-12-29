# Resume Converter - Quick Start Examples

## Prerequisites

Good news! All required packages are already installed:
- ✓ PyPDF2 (v3.0.1)
- ✓ python-docx (v1.1.0)
- ✓ google-generativeai (for Gemini AI)

## Quick Start

### 1. Convert a Resume to JSON

```bash
# Convert PDF resume
python resume_converter.py --input resume.pdf

# Convert DOCX resume
python resume_converter.py --input resume.docx

# Convert TXT resume
python resume_converter.py --input resume.txt
```

**What happens:**
- Extracts text from your resume
- Uses Gemini AI to intelligently structure the information
- Creates a JSON file in `data/resumes/` directory
- Validates all required fields are present

### 2. Specify Custom Output Location

```bash
python resume_converter.py --input resume.pdf --output my_custom_resume.json
```

### 3. Override Candidate Name

```bash
python resume_converter.py --input resume.pdf --name "John Doe"
```

Useful if the AI doesn't extract the name correctly.

### 4. Optimize for a Specific Job

**Step 1**: Create job JSON from job description

```bash
python main.py --mode process-description --job-description sdet_job.txt --output-type save_json_only
```

This creates `data/jobs/SDET_job.json`

**Step 2**: Convert and optimize resume

```bash
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/SDET_job.json
```

**What optimization does:**
- Highlights skills matching the job description
- Emphasizes relevant experience
- Adds **bold markers** to key terms
- Tailors professional summary to the role
- Prioritizes matching competencies

## Complete Workflow Example

### Scenario: Apply for an SDET Position

```bash
# 1. You have: resume.pdf and job_description.txt

# 2. Convert job description to JSON
python main.py --mode process-description --job-description job_description.txt --output-type save_json_only

# 3. Convert your resume to JSON (optimized for the job)
python resume_converter.py \
  --input resume.pdf \
  --optimize \
  --job-file data/jobs/SDET_job.json \
  --output data/resumes/sdet_optimized_resume.json

# 4. Generate final resume DOCX and cover letter
python main.py --mode resume --job-file data/jobs/SDET_job.json

# 5. Your files are ready in data/resumes/!
```

## Sample Resume Formats

### PDF Format
```
Your resume.pdf with standard sections:
- Contact Information
- Professional Summary
- Skills
- Work Experience
- Education
```

### DOCX Format
```
Your resume.docx with typical structure:
- Header with name and contact
- Summary/Objective
- Technical Skills
- Professional Experience
- Education
- Certifications
```

### TXT Format
```
JOHN DOE
Email: john@example.com | Phone: (123) 456-7890

PROFESSIONAL SUMMARY
Senior SDET with 10 years of experience...

SKILLS
Java, Python, Selenium, AWS, Docker...

EXPERIENCE
Company Name - Senior SDET (2020-Present)
- Achievement 1
- Achievement 2

EDUCATION
MBA in Information Technology
University Name, 2016
```

## Expected Output Structure

After conversion, you'll get a JSON file like this:

```json
{
  "header": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(123) 456-7890",
    "citizenship": "US Citizen",
    "linkedin": "linkedin.com/in/johndoe"
  },
  "professional_summary": {
    "title_experience": "**Senior SDET** with **10+ years** of experience...",
    "track_record": "Reduced defects by **75%** and achieved **80% automation coverage**...",
    "expertise": "Expert in **test automation**, **CI/CD**, and **cloud testing**...",
    "core_value": "Transform manual processes into scalable automated solutions..."
  },
  "core_competencies": {
    "programming_and_automation": ["**Java**", "**Python**", "JavaScript"],
    "testing_frameworks": ["**Selenium**", "**REST Assured**", "Appium"],
    ...
  },
  "professional_experience": [...],
  "education": [...]
}
```

## Using with Existing SmartApplyPro Features

### 1. Set as Your Default Resume

```bash
# Replace the default template
copy data\resumes\your_resume.json zahid_resume_v2.json
```

Now all automated applications will use your resume!

### 2. Generate Resumes for Multiple Jobs

```bash
# Convert multiple job descriptions
python main.py --mode process-description --job-description job1.txt --output-type save_json_only
python main.py --mode process-description --job-description job2.txt --output-type save_json_only

# Generate optimized resumes for each
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/job1.json
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/job2.json
```

### 3. Automated Job Application

```bash
# 1. Set your resume as default
copy data\resumes\your_resume.json zahid_resume_v2.json

# 2. Run automated job search and apply
python main.py --mode auto
```

## Tips for Best Results

### 1. Resume Formatting

For best AI extraction:
- Use clear section headings (Experience, Education, Skills)
- Include dates in standard format (Jan 2020 - Present)
- List skills clearly
- Include contact information at the top
- Use bullet points for achievements

### 2. Job Description Optimization

When optimizing for a job:
- Ensure the job JSON has a good skills list
- The AI will highlight matching skills with **bold**
- Review the output and adjust if needed

### 3. Manual Editing

After conversion, you can:
- Open the JSON file in any text editor
- Fix any incorrectly extracted information
- Add missing details
- Adjust formatting

### 4. Testing

Before using in production:
```bash
# Test the conversion
python resume_converter.py --input resume.pdf

# Review the output
notepad data\resumes\Your_Name_resume.json

# Generate a test resume DOCX
python main.py --mode resume --job-file data/jobs/test_job.json
```

## Troubleshooting

### Common Issues

**Issue**: Name extracted incorrectly
```bash
# Solution: Specify it manually
python resume_converter.py --input resume.pdf --name "Correct Name"
```

**Issue**: Missing skills or experience
```bash
# Solution: Edit the JSON file manually after conversion
notepad data\resumes\resume.json
```

**Issue**: AI extraction failed
```bash
# Check the error log and try again
# AI responses can vary, sometimes a retry works
python resume_converter.py --input resume.pdf
```

## API Usage

Each conversion uses Gemini AI API calls:
- **Basic conversion**: 1 API call
- **With optimization**: 4 API calls (extraction + 3 sections)

Daily limit per API key: 800 calls
You have 2 API keys configured = 1,600 calls/day

This means you can convert approximately:
- 1,600 basic conversions per day
- 400 optimized conversions per day

## Next Steps

1. Try converting your resume
2. Review and edit the JSON output
3. Use it with SmartApplyPro's resume generator
4. Optimize for specific jobs you're targeting
5. Automate your job applications!

---

Ready to get started? Run:

```bash
python resume_converter.py --input your_resume.pdf
```
