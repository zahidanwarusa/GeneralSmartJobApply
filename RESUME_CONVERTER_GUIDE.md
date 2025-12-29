# Resume Converter Guide

## Overview

`resume_converter.py` is a powerful tool that converts resumes in various formats (PDF, DOCX, TXT) to the structured JSON format used by SmartApplyPro, with AI-powered extraction and optimization using Google Gemini.

## Features

- **Multi-Format Support**: Convert PDF, DOCX, and TXT files
- **AI-Powered Extraction**: Uses Gemini AI to intelligently extract and structure resume information
- **Job-Specific Optimization**: Optionally optimize resume for specific job descriptions
- **Automatic Validation**: Ensures all required fields are present
- **Template Matching**: Follows the exact structure used by SmartApplyPro

## Installation

### Required Dependencies

Install the required Python packages:

```bash
pip install PyPDF2 python-docx
```

These are needed for:
- `PyPDF2`: Extract text from PDF files
- `python-docx`: Extract text from DOCX files

## Usage

### Basic Commands

#### 1. Convert a Resume (Basic)

```bash
python resume_converter.py --input resume.pdf
```

This will:
- Extract text from the resume
- Use AI to convert it to JSON format
- Save to `data/resumes/{name}_resume.json`

#### 2. Specify Output File

```bash
python resume_converter.py --input resume.docx --output my_resume.json
```

#### 3. Specify Candidate Name

```bash
python resume_converter.py --input resume.txt --name "John Doe"
```

This overrides the name extracted from the resume.

#### 4. Convert and Optimize for a Job

```bash
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/sdet_job.json
```

This will:
- Convert the resume to JSON
- Optimize it based on the job description
- Highlight relevant skills and experience
- Save the optimized version

#### 5. Complete Workflow

```bash
python resume_converter.py --input resume.pdf --output custom.json --name "Jane Smith" --optimize --job-file data/jobs/job.json
```

## JSON Structure

The converter creates a JSON file with this structure:

```json
{
  "header": {
    "name": "Your Name",
    "email": "email@example.com",
    "phone": "(123) 456-7890",
    "citizenship": "US Citizen",
    "linkedin": "linkedin.com/in/yourprofile"
  },
  "professional_summary": {
    "title_experience": "Senior SDET with 10+ years...",
    "track_record": "Proven track record of...",
    "expertise": "Expert in cloud-native testing...",
    "core_value": "Transform manual testing processes..."
  },
  "core_competencies": {
    "programming_and_automation": ["Java", "Python", "JavaScript"],
    "testing_frameworks": ["Selenium", "REST Assured", "Appium"],
    "cloud_and_devops": ["AWS", "Docker", "Kubernetes"],
    "api_and_performance": ["REST APIs", "JMeter", "Postman"],
    "quality_tools": ["Maven", "Gradle", "Jira"],
    "databases": ["Oracle", "MySQL", "PostgreSQL"],
    "domain_expertise": ["Healthcare", "Financial Services"],
    "leadership": ["Team Mentoring", "Technical Strategy"]
  },
  "professional_experience": [
    {
      "company": "Company Name",
      "location": "City, State",
      "position": "Job Title",
      "duration": "Jan 2020 - Present",
      "summary": "Brief role overview...",
      "key_achievements": [
        "Achievement 1 with **metrics**",
        "Achievement 2 with **impact**"
      ],
      "detailed_achievements": [
        "Detailed achievement 1...",
        "Detailed achievement 2..."
      ],
      "environment": "Java, Selenium, AWS, Docker, Jenkins"
    }
  ],
  "education": [
    {
      "degree": "MBA",
      "major": "Information Technology",
      "university": "University Name",
      "year": "2016"
    }
  ]
}
```

## How It Works

### 1. Text Extraction

The tool automatically detects the file format and extracts text:

- **PDF**: Uses PyPDF2 to extract text from all pages
- **DOCX**: Uses python-docx to extract text from paragraphs and tables
- **TXT**: Direct text reading with encoding detection

### 2. AI-Powered Conversion

The extracted text is sent to Google Gemini AI with:
- The template structure from `zahid_resume_v2.json`
- Instructions for organizing information
- Guidelines for formatting (bold markers, etc.)

### 3. Validation & Cleanup

The tool:
- Validates all required sections are present
- Ensures proper data types (arrays, objects)
- Adds placeholders for missing information
- Formats dates and text consistently

### 4. Optional Optimization

If `--optimize` is used:
- Loads the job description JSON
- Optimizes professional summary for the job
- Highlights relevant skills in core competencies
- Emphasizes matching experience
- Adds bold markers to key terms

## Integration with SmartApplyPro

Once converted, use your JSON resume with SmartApplyPro:

### 1. Set as Default Resume

```bash
# Copy to default location
copy my_resume.json zahid_resume_v2.json
```

### 2. Generate Optimized Resume for a Job

```bash
python main.py --mode resume --job-file data/jobs/job.json
```

### 3. Full Application Workflow

```bash
# 1. Convert your resume
python resume_converter.py --input resume.pdf

# 2. Convert job description
python main.py --mode process-description --job-description job.txt --output-type save_json_only

# 3. Generate optimized resume and cover letter
python main.py --mode process-description --job-description job.txt --output-type generate_both
```

## Command-Line Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--input` | `-i` | Input resume file (PDF/DOCX/TXT) | Yes |
| `--output` | `-o` | Output JSON file path | No |
| `--name` | `-n` | Candidate name to use | No |
| `--optimize` | - | Optimize with job description | No |
| `--job-file` | `-j` | Job JSON for optimization | If --optimize |

## Examples

### Example 1: Convert PDF Resume

```bash
python resume_converter.py --input "John_Doe_Resume.pdf"
```

**Output**: `data/resumes/John_Doe_resume.json`

### Example 2: Convert and Customize

```bash
python resume_converter.py \
  --input "resume.docx" \
  --output "data/resumes/custom_resume.json" \
  --name "Jane Smith"
```

### Example 3: Convert and Optimize for SDET Role

```bash
# First, create job JSON
python main.py --mode process-description --job-description sdet_job.txt --output-type save_json_only

# Then convert and optimize resume
python resume_converter.py \
  --input resume.pdf \
  --optimize \
  --job-file data/jobs/SDET_job.json
```

### Example 4: Batch Processing

```bash
# Convert multiple resumes
for file in *.pdf; do
  python resume_converter.py --input "$file"
done
```

## Troubleshooting

### Issue: "PyPDF2 not installed"

**Solution**: Install required package
```bash
pip install PyPDF2
```

### Issue: "python-docx not installed"

**Solution**: Install required package
```bash
pip install python-docx
```

### Issue: "Failed to parse JSON from AI response"

**Cause**: AI didn't generate valid JSON

**Solution**:
1. Check `data/resumes/failed_extraction.txt` for the raw response
2. Try again (AI responses can vary)
3. Ensure your resume has clear structure

### Issue: Missing sections in output

**Solution**: The tool adds default placeholders. You can manually edit the JSON to fill in missing information.

### Issue: Name not extracted correctly

**Solution**: Use the `--name` parameter to specify it manually:
```bash
python resume_converter.py --input resume.pdf --name "Your Name"
```

## Tips for Best Results

1. **Clean Resume Format**: Use well-structured resumes with clear sections
2. **Standard Headings**: Use common headings like "Experience", "Education", "Skills"
3. **Review Output**: Always review the JSON output and edit if needed
4. **Test Optimization**: Try optimizing for different jobs to see variations
5. **Keep Template Updated**: If you modify `zahid_resume_v2.json`, it will affect future conversions

## Advanced Usage

### Using as a Python Module

```python
from resume_converter import ResumeConverter

# Initialize converter
converter = ResumeConverter()

# Extract text
text = converter.extract_text_from_file("resume.pdf")

# Convert to JSON
resume_json = converter.convert_to_json(text, candidate_name="John Doe")

# Optimize for job
optimized = converter.optimize_with_job_description(
    resume_json,
    "data/jobs/job.json"
)

# Save
converter.save_json(optimized, "output.json")
```

### Customizing the Conversion

You can modify the prompt in the `convert_to_json` method to:
- Emphasize certain sections
- Change formatting preferences
- Add custom fields
- Modify extraction logic

## API Usage Tracking

The converter uses the same Gemini API key rotation system as SmartApplyPro:

- Daily limit: 800 requests per API key
- Automatic key rotation when limits reached
- Warning at 85% usage
- Check usage: See the logs during conversion

Each conversion typically uses:
- 1 API call for initial extraction
- 3 API calls if optimizing (summary, competencies, experience)

## Next Steps

After converting your resume:

1. **Review the JSON**: Open in text editor and verify accuracy
2. **Test with SmartApplyPro**: Generate a sample resume
3. **Optimize for Jobs**: Use the optimization feature for targeted applications
4. **Automate**: Integrate into your job application workflow

## Support

For issues or questions:
1. Check the logs in the console output
2. Review `debug/` folder for AI responses
3. Examine `data/resumes/failed_extraction.txt` if conversion fails
4. Ensure all dependencies are installed

---

**Happy Job Hunting! 🚀**
