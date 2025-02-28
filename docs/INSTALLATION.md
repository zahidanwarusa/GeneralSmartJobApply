# SmartApplyPro Installation Guide

This guide will walk you through the complete installation and setup process for SmartApplyPro.

## Prerequisites

Before installing SmartApplyPro, ensure you have the following:

1. **Python 3.9+** installed on your system
2. **Google Chrome** browser installed
3. **Git** for cloning the repository
4. **Google Gemini API key** for AI-powered optimizations

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/SmartApplyPro.git
cd SmartApplyPro
```

## Step 2: Set Up a Virtual Environment (Recommended)

Creating a virtual environment keeps your dependencies isolated:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available, install the required packages manually:

```bash
pip install selenium python-docx google-generativeai
```

## Step 4: Install ChromeDriver

1. Check your Chrome version by navigating to `chrome://version/` in your Chrome browser
2. Download the matching ChromeDriver version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/)
3. Extract the downloaded file and place the chromedriver executable in the `webdriver` folder of the project

## Step 5: Configure the Application

1. Create a copy of `config.sample.py` and name it `config.py`
2. Update the following settings in `config.py`:

```python
# Chrome profile settings
CHROME_PROFILE = {
    'user_data_dir': 'C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data',
    'profile_directory': 'Profile 1'  # Or your preferred profile
}

# API key for Google Gemini
GEMINI_API_KEY = 'your-api-key-here'

# Customize job search parameters if needed
JOB_TITLES = [
    "SDET",
    "Software Development Engineer in Test",
    # Add or remove job titles as needed
]
```

## Step 6: Set Up Your Default Resume

1. Review the `default-resume-main.json` file and update it with your personal information
2. Ensure all sections accurately reflect your professional background

## Step 7: Verify Installation

Run a simple test to verify that the installation was successful:

```bash
python main.py --mode list
```

If everything is set up correctly, you should see a message indicating that no applications have been tracked yet.

## Troubleshooting

### Chrome Profile Issues

If you encounter issues with the Chrome profile:

1. Create a new Chrome profile specifically for SmartApplyPro
2. Update the `CHROME_PROFILE` settings in `config.py`
3. Make sure Chrome is completely closed before running the application

### ChromeDriver Compatibility

If you see WebDriver errors:

1. Verify that your ChromeDriver version matches your Chrome browser version
2. Update the path in `config.py` if you placed ChromeDriver in a different location

### API Key Issues

If AI features are not working:

1. Verify your Gemini API key is correct
2. Ensure you have billing set up for the Gemini API
3. Check if there are any usage limits that might be affecting your requests

## Next Steps

Once installation is complete, refer to the [User Guide](./USER_GUIDE.md) for detailed instructions on how to use SmartApplyPro for your job application needs.