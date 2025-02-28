import os
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
RESUME_DIR = DATA_DIR / 'resumes'
JOBS_DIR = DATA_DIR / 'jobs'
TEMP_DIR = DATA_DIR / 'temp'

# Create directories if they don't exist
for directory in [DATA_DIR, RESUME_DIR, JOBS_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default resume template
DEFAULT_RESUME = BASE_DIR / 'default-resume-main.json'
if not DEFAULT_RESUME.exists():
    raise FileNotFoundError(f"Default resume template not found: {DEFAULT_RESUME}")

# API Keys
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY_HERE'  # Replace with your key

# Chrome Settings
CHROME_PROFILE = {
    'user_data_dir': 'C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data',
    'profile_directory': 'Profile 1'
}

# ChromeDriver path
CHROMEDRIVER_PATH = "webdriver\\chromedriver.exe"

# Chrome startup arguments
CHROME_ARGUMENTS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-blink-features=AutomationControlled'
]

# Application Settings
DELAYS = {
    'page_load': (4, 8),
    'between_actions': (2, 5),
    'between_applications': (8, 15),
    'between_pages': (5, 10)
}

MAX_RETRIES = {
    'click': 3,
    'form': 2,
    'page_load': 2
}

# Job Search Settings
JOB_TITLES = [
    "SDET",
    "Software Development Engineer in Test",
    "Automation Engineer",
    "QA Automation Engineer",
    "Test Automation Engineer",
    "Senior SDET",
    "Lead SDET"
]

# Search URL template
DICE_SEARCH_URL = "https://www.dice.com/jobs?q={}&countryCode=US&radius=30&radiusUnit=mi&pageSize=20&filters.workplaceTypes=Remote&filters.easyApply=true&language=en"