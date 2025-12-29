# Resume to JSON Converter

Convert any resume format (PDF, DOCX, TXT) to the structured JSON format used by SmartApplyPro, with AI-powered extraction and job-specific optimization.

## Features

✨ **Multi-Format Support**
- PDF files (using PyPDF2)
- DOCX files (using python-docx)
- TXT files (plain text)

🤖 **AI-Powered Extraction**
- Uses Google Gemini AI to intelligently extract and structure resume information
- Automatically organizes information into required sections
- Validates and fills missing fields

🎯 **Job-Specific Optimization**
- Optimize resume for specific job descriptions
- Highlight relevant skills and experience
- Tailored professional summaries
- Strategic keyword placement with bold markers

✅ **Quality Assurance**
- Validates all required sections
- Ensures proper data structure
- Adds reasonable defaults for missing information
- Compatible with SmartApplyPro's resume generator

## Quick Start

### Installation

All required packages are already installed! ✓
- PyPDF2 (v3.0.1)
- python-docx (v1.1.0)
- google-generativeai

### Basic Usage

```bash
# Convert a resume to JSON
python resume_converter.py --input resume.pdf

# Convert with custom output file
python resume_converter.py --input resume.docx --output my_resume.json

# Convert with custom name
python resume_converter.py --input resume.txt --name "John Doe"

# Convert and optimize for a job
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/job.json
```

## Documentation

📚 **Complete Guides**:
- `RESUME_CONVERTER_GUIDE.md` - Detailed documentation
- `example_resume_conversion.md` - Quick start examples and workflows

## Common Workflows

### Workflow 1: Basic Conversion

```bash
python resume_converter.py --input resume.pdf
```

Output: `data/resumes/Your_Name_resume.json`

### Workflow 2: Optimized for Job Application

```bash
# Step 1: Convert job description to JSON
python main.py --mode process-description --job-description job.txt --output-type save_json_only

# Step 2: Convert and optimize your resume
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/job.json

# Step 3: Generate final resume DOCX
python main.py --mode resume --job-file data/jobs/job.json
```

### Workflow 3: Set as Default Resume

```bash
# Convert your resume
python resume_converter.py --input resume.pdf --output zahid_resume_v2.json

# Now SmartApplyPro will use your resume for all applications!
python main.py --mode auto
```

## Command-Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--input` / `-i` | Input resume file (PDF/DOCX/TXT) | Yes |
| `--output` / `-o` | Output JSON file path | No |
| `--name` / `-n` | Candidate name (override extracted name) | No |
| `--optimize` | Optimize resume for job description | No |
| `--job-file` / `-j` | Job description JSON file | If --optimize |

## JSON Structure

The converter creates a structured JSON with these sections:

```
{
  header                 → Name, email, phone, linkedin
  professional_summary   → Title, track record, expertise, value
  core_competencies      → 8 categories of skills
  professional_experience → Work history with achievements
  education              → Degrees and certifications
}
```

See `zahid_resume_v2.json` for the complete template.

## Integration with SmartApplyPro

Once you have your JSON resume:

1. **Use it directly**: `copy resume.json zahid_resume_v2.json`
2. **Generate optimized resumes**: `python main.py --mode resume --job-file job.json`
3. **Automate applications**: `python main.py --mode auto`

## Examples

### Example 1: First-Time Setup

```bash
# Convert your resume
python resume_converter.py --input "MyResume.pdf" --name "John Doe"

# Review the output
notepad data\resumes\John_Doe_resume.json

# Set as default
copy data\resumes\John_Doe_resume.json zahid_resume_v2.json

# Test it
python main.py --mode process-description --job-description test_job.txt --output-type generate_both
```

### Example 2: Optimizing for Multiple Jobs

```bash
# Convert multiple job descriptions
python main.py --mode process-description --job-description sdet_job.txt --output-type save_json_only
python main.py --mode process-description --job-description qa_job.txt --output-type save_json_only

# Create optimized resume for each
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/SDET_job.json --output sdet_resume.json
python resume_converter.py --input resume.pdf --optimize --job-file data/jobs/QA_job.json --output qa_resume.json
```

### Example 3: Batch Processing

```bash
# Convert all PDF resumes in a folder
for %f in (*.pdf) do python resume_converter.py --input "%f"
```

## How It Works

1. **Extract Text**: Reads content from PDF, DOCX, or TXT
2. **AI Processing**: Sends to Gemini AI with structured template
3. **JSON Creation**: Receives structured JSON response
4. **Validation**: Ensures all required fields are present
5. **Optimization** (optional): Tailors content to job description
6. **Save**: Writes formatted JSON to file

## Tips for Best Results

✓ Use well-structured resumes with clear sections
✓ Include standard headings (Experience, Education, Skills)
✓ Format dates consistently
✓ List skills clearly
✓ Review and edit JSON output if needed
✓ Test with sample job before production use

## API Usage

- **Basic conversion**: 1 Gemini API call
- **With optimization**: 4 API calls
- **Daily limit**: 800 calls per API key (2 keys = 1,600/day)

## Troubleshooting

**Q: Name not extracted correctly?**
A: Use `--name "Your Name"` parameter

**Q: Missing information?**
A: Edit the JSON file manually after conversion

**Q: Conversion failed?**
A: Check `data/resumes/failed_extraction.txt` and try again

**Q: How to review output?**
A: Open the JSON file in any text editor

## Support Files

- `resume_converter.py` - Main converter script
- `RESUME_CONVERTER_GUIDE.md` - Complete documentation
- `example_resume_conversion.md` - Quick examples
- `zahid_resume_v2.json` - Template structure

## Success Metrics

After conversion, you can:
- ✓ Generate unlimited optimized resumes for different jobs
- ✓ Automate job applications with your own information
- ✓ Maintain consistency across all applications
- ✓ Quickly update and re-convert when resume changes

## Getting Help

1. Read `RESUME_CONVERTER_GUIDE.md` for detailed information
2. Check `example_resume_conversion.md` for workflow examples
3. Review logs and debug output if issues occur
4. Verify JSON structure against `zahid_resume_v2.json`

---

**Ready to start?**

```bash
python resume_converter.py --input your_resume.pdf
```

Then check the output in `data/resumes/`!

---

*Built with ❤️ for SmartApplyPro - AI-Powered Job Application Automation*
