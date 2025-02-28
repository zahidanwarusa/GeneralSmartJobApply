# SmartApplyPro User Guide

This comprehensive guide explains how to effectively use SmartApplyPro to optimize your job search and application process.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running Automated Job Applications](#running-automated-job-applications)
3. [Creating Optimized Resumes](#creating-optimized-resumes)
4. [Generating Cover Letters](#generating-cover-letters)
5. [Tracking Applications](#tracking-applications)
6. [Customizing Your Experience](#customizing-your-experience)
7. [Tips for Success](#tips-for-success)
8. [Troubleshooting](#troubleshooting)

## Getting Started

After completing the installation process outlined in the [Installation Guide](./INSTALLATION.md), you're ready to start using SmartApplyPro.

### First-Time Setup Checklist

1. **Chrome Profile**: Ensure you're logged into your Dice.com account in the Chrome profile you configured
2. **Resume Template**: Customize the default resume template in `default-resume-main.json`
3. **Job Search Parameters**: Review and update job search parameters in `config.py`

## Running Automated Job Applications

The automated job application feature searches for relevant positions on Dice.com and applies to them using your optimized resume and cover letter.

### Starting the Automated Process

```bash
python main.py --mode auto
```

This command will:
1. Search for jobs matching your configured job titles
2. Filter for remote positions with Easy Apply enabled
3. Generate tailored resumes and cover letters for each suitable position
4. Submit applications automatically
5. Track all applications in the system

### Monitoring Progress

During automation, SmartApplyPro will create detailed logs in the `logs/` directory. You can monitor the current session's progress in the console output.

### Stopping the Process

The automated process can be stopped at any time by pressing `Ctrl+C` in the terminal. Any completed applications will be saved in the system.

## Creating Optimized Resumes

SmartApplyPro can generate job-specific optimized resumes from a single job description file.

### Creating a Job Description File

First, create a JSON file with the job details. Save it in the `data/jobs/` directory.

```json
{
  "title": "Senior SDET",
  "company": "Example Company",
  "description": "Detailed job description...",
  "skills": [
    "Selenium",
    "Java",
    "Test Automation",
    "CI/CD",
    "API Testing"
  ]
}
```

### Generating the Resume

```bash
python main.py --mode resume --job-file data/jobs/your-job-file.json
```

This will:
1. Analyze the job description and required skills
2. Optimize your resume content to highlight relevant experience
3. Format the resume professionally
4. Save both .docx and .json versions in the `data/resumes/` directory

## Generating Cover Letters

SmartApplyPro can create tailored cover letters based on a job description and your resume.

```bash
python main.py --mode cover --job-file data/jobs/your-job-file.json --resume data/resumes/your-resume.docx
```

This will:
1. Analyze both the job description and your resume
2. Generate a personalized cover letter highlighting your most relevant qualifications
3. Save the cover letter as a text file in the `data/jobs/` directory

## Tracking Applications

To view all tracked job applications:

```bash
python main.py --mode list
```

This will display:
- Job titles and companies
- Application dates
- Whether a customized resume was created
- Whether a cover letter was generated

## Customizing Your Experience

### Modifying Job Search Parameters

Edit the `config.py` file to customize:
- Job titles to search for
- Search radius
- Workplace types (remote, hybrid, on-site)
- Results per page

### Customizing Your Base Resume

The `default-resume-main.json` file serves as your base resume. Modify this file to:
- Update your personal information
- Add new skills or experiences
- Adjust your career summary
- Update your education details

## Tips for Success

### Optimizing Your Chrome Profile

1. **Clean Browser State**: Start with a fresh Chrome profile for best results
2. **Pre-login**: Ensure you're logged into Dice.com before running the automation
3. **Save Password**: Allow Chrome to save your Dice.com password for smoother automation

### Improving Resume Optimization

1. **Comprehensive Base Resume**: Include all your experiences and skills in the default resume
2. **Specific Achievements**: Use concrete numbers and achievements in your work descriptions
3. **Keyword Variety**: Include various forms of key skills (e.g., "Selenium," "Selenium WebDriver")

### Maximizing Application Success

1. **Strategic Timing**: Run automations during business hours when new jobs are posted
2. **Regular Updates**: Keep your base resume updated with your latest experiences
3. **Selective Application**: Focus on quality matches rather than quantity of applications

## Troubleshooting

### Common Issues and Solutions

#### Application Process Stops Unexpectedly

**Possible causes and solutions:**
- **Browser closed or crashed**: Restart the application
- **Network interruption**: Check your internet connection
- **Website structure changed**: Check for updates to SmartApplyPro

#### Resume Generation Fails

**Possible causes and solutions:**
- **API key issues**: Verify your Gemini API key
- **Format problems in job description**: Ensure job description JSON is properly formatted
- **Error in base resume**: Check for formatting issues in default-resume-main.json

#### Browser Automation Errors

**Possible causes and solutions:**
- **ChromeDriver version mismatch**: Update ChromeDriver to match your Chrome version
- **Element not found errors**: Website may have changed; check for SmartApplyPro updates
- **Login issues**: Ensure your Chrome profile has a valid Dice.com login