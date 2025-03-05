import os
import json
import time
import random
import logging
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from urllib.parse import quote
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

from config import (
    CHROME_PROFILE, 
    CHROME_ARGUMENTS,
    CHROMEDRIVER_PATH,
    DELAYS, 
    MAX_RETRIES, 
    JOB_TITLES,
    DICE_SEARCH_URL,
    JOBS_DIR,
    RESUME_DIR,
    DATA_DIR
)
from resume_handler import ResumeHandler
from gemini_service import GeminiService
from application_tracker import ApplicationTracker

class DiceBot:
    """Automated job application bot for Dice.com with enhanced workflow and tracking"""
    
    def __init__(self):
        self.setup_logging()
        self.resume_handler = ResumeHandler()
        self.gemini = GeminiService()
        self.tracker = ApplicationTracker(DATA_DIR)
        self.driver = None
        self.wait = None
        self.jobs_processed = 0
        self.jobs_applied = 0
        self.jobs_skipped = 0
        
    def setup_logging(self):
        """Configure logging"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        fh = logging.FileHandler(
            log_dir / f'dice_bot_{datetime.now():%Y%m%d_%H%M%S}.log'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def setup_driver(self) -> bool:
        """Initialize Chrome WebDriver with enhanced anti-detection measures"""
        try:
            options = Options()
            
            # Set profile paths
            user_data_dir = CHROME_PROFILE['user_data_dir']
            profile_directory = CHROME_PROFILE['profile_directory']
            
            # Basic Chrome options
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument(f'--profile-directory={profile_directory}')
            
            # Window management options
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            options.add_argument('--window-size=1920,1080')
            
            # SSL and security options
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--ignore-ssl-errors')
            
            # Graphics and performance options
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-webgl')
            
            # Anti-detection options (enhanced)
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('detach', True)
            
            # Additional stability options
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            
            # Add User-Agent to appear as regular browser
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            
            # Initialize ChromeDriver service with additional logging
            service = Service(
                executable_path=CHROMEDRIVER_PATH,
                log_path="logs/chromedriver.log"
            )
            
            # Create logging directory
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            
            # Close any existing Chrome processes (more safely)
            try:
                if os.name == 'nt':  # Windows
                    os.system("taskkill /f /im chrome.exe")
                else:  # Linux/Mac
                    os.system("pkill -f chrome")
                time.sleep(2)
            except:
                self.logger.warning("Failed to kill Chrome processes, continuing anyway")
            
            # Initialize driver
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 15)
            
            # Enhanced anti-detection script
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    // Override webdriver property
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    // Override chrome property
                    Object.defineProperty(window, 'chrome', {
                        value: {
                            runtime: {}
                        }
                    });
                    
                    // Override permissions
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                    
                    // Add language plugins to appear more human-like
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en', 'es-ES', 'es']
                    });
                    
                    // Add random mouse movements simulation
                    setInterval(() => {
                        const randomX = Math.floor(Math.random() * window.innerWidth);
                        const randomY = Math.floor(Math.random() * window.innerHeight);
                        const mouseEvent = new MouseEvent('mousemove', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: randomX,
                            clientY: randomY
                        });
                        document.dispatchEvent(mouseEvent);
                    }, 10000);
                '''
            })
            
            # Wait for window to be properly initialized
            time.sleep(3)
            self.driver.maximize_window()
            
            # Create debug directory
            debug_dir = Path('debug')
            debug_dir.mkdir(exist_ok=True)
            
            self.logger.info("WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            return False
    
    def random_delay(self, delay_type: str):
        """Add random delay between actions"""
        min_delay, max_delay = DELAYS.get(delay_type, (2, 5))
        time.sleep(random.uniform(min_delay, max_delay))


    def get_job_id_from_card(self, card) -> Optional[str]:
        """Extract job ID from card without opening job details"""
        try:
            # Try to get a unique identifier from the card itself
            title_link = None
            job_url = None
            
            try:
                title_link = card.find_element(
                    By.CSS_SELECTOR,
                    "[data-cy='card-title-link']"
                )
                if title_link:
                    job_url = title_link.get_attribute('href')
            except NoSuchElementException:
                # Try alternative selectors
                for selector in [".card-title-link", "a.job-title", "h2 a", "h3 a"]:
                    try:
                        title_link = card.find_element(By.CSS_SELECTOR, selector)
                        if title_link:
                            job_url = title_link.get_attribute('href')
                            break
                    except:
                        continue
            
            # Check if we found a URL
            if job_url:
                # Extract job ID from URL or generate a hash from the URL
                if '/jobs/' in job_url:
                    job_id = job_url.split('/jobs/')[1].split('/')[0]
                else:
                    # Create a hash if we can't extract a nice ID
                    job_id = hashlib.md5(job_url.encode()).hexdigest()
                
                return job_id
            else:
                # If we couldn't get a URL, create a hash from the card text
                card_text = card.text
                if card_text:
                    return hashlib.md5(card_text.encode()).hexdigest()
                else:
                    return f"unknown_{self.jobs_processed}"
            
        except Exception as e:
            self.logger.warning(f"Could not extract job ID from card: {str(e)}")
            return f"unknown_{self.jobs_processed}"

    def check_easy_apply_available(self, card) -> bool:
        """Check if Easy Apply is available with improved shadow DOM support"""
        try:
            # Debug: Save the card HTML
            try:
                card_html = card.get_attribute('outerHTML')
                card_index = self.jobs_processed
                debug_dir = Path('debug/easy_apply')
                debug_dir.mkdir(parents=True, exist_ok=True)
                with open(f'debug/easy_apply/card_{card_index}.html', 'w', encoding='utf-8') as f:
                    f.write(card_html)
            except:
                pass
                
            # Method 1: Check for apply-button-wc web component
            apply_buttons = card.find_elements(By.TAG_NAME, "apply-button-wc")
            if apply_buttons:
                for apply_button in apply_buttons:
                    # First check if it's already applied through shadow DOM
                    is_applied = self.driver.execute_script("""
                        const applyButton = arguments[0];
                        
                        // Access the shadow root
                        if (!applyButton.shadowRoot) return false;
                        
                        // Look for application-submitted component
                        const appSubmitted = applyButton.shadowRoot.querySelector('application-submitted');
                        if (appSubmitted) return true;
                        
                        // Check for any text indicating application status
                        const shadowText = applyButton.shadowRoot.textContent.toLowerCase();
                        return shadowText.includes('application submitted') || 
                            shadowText.includes('applied') ||
                            shadowText.includes('app submitted');
                    """, apply_button)
                    
                    if is_applied:
                        self.logger.info("Job already applied through shadow DOM check")
                        return False
                    
                    # If not applied, check if it has an apply button in shadow DOM
                    has_apply = self.driver.execute_script("""
                        const applyButton = arguments[0];
                        
                        // Access the shadow root
                        if (!applyButton.shadowRoot) return false;
                        
                        // Look for standard button element
                        const button = applyButton.shadowRoot.querySelector('button');
                        if (button) return true;
                        
                        // Or any element with 'apply' in its class or text
                        const applyElements = Array.from(applyButton.shadowRoot.querySelectorAll('*')).filter(el => {
                            if (el.className && el.className.toLowerCase().includes('apply')) return true;
                            if (el.textContent && el.textContent.toLowerCase().includes('apply')) return true;
                            return false;
                        });
                        
                        return applyElements.length > 0;
                    """, apply_button)
                    
                    if has_apply:
                        self.logger.info("Found Easy Apply in shadow DOM")
                        return True
            
            # Method 2: Look for standard Easy Apply indicators
            easy_apply_indicators = [
                "[data-cy='easyApplyBtn']",
                ".easy-apply-button",
                ".easy-apply",
                "button[class*='easyApply']",
                "button[class*='easy-apply']",
                "a[class*='easyApply']",
                "a[class*='easy-apply']"
            ]
            
            for indicator in easy_apply_indicators:
                try:
                    elements = card.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                self.logger.info(f"Found Easy Apply with selector: {indicator}")
                                return True
                except:
                    continue
            
            # Method 3: Look for "Easy Apply" text in any element
            try:
                easy_apply_elements = card.find_elements(By.XPATH, ".//*[contains(translate(text(), 'EASY APPLY', 'easy apply'), 'easy apply')]")
                if easy_apply_elements:
                    for element in easy_apply_elements:
                        if element.is_displayed():
                            self.logger.info("Found Easy Apply text in element")
                            return True
            except:
                pass
            
            # Method 4: Check any button or link with "apply" text
            try:
                buttons_and_links = card.find_elements(By.CSS_SELECTOR, "button, a")
                for element in buttons_and_links:
                    try:
                        element_text = element.text.lower()
                        element_class = element.get_attribute('class') or ''
                        
                        # Skip if it contains "applied" text
                        if 'applied' in element_text:
                            continue
                            
                        # Check for apply text or class
                        if ('apply' in element_text and element.is_displayed()) or \
                        ('apply' in element_class.lower() and element.is_displayed()):
                            self.logger.info(f"Found button/link with apply: {element_text}")
                            return True
                    except:
                        continue
            except:
                pass
                
            # If we find text in the card indicating it's Easy Apply
            try:
                card_text = card.text.lower()
                if 'easy apply' in card_text and 'applied' not in card_text:
                    # Additional verification - check if there's actually a button
                    buttons = card.find_elements(By.TAG_NAME, "button")
                    if buttons and any(b.is_displayed() for b in buttons):
                        self.logger.info("Found 'Easy Apply' text in card")
                        return True
            except:
                pass
            
            # Debug: Log what we found in the card
            try:
                with open(f'debug/easy_apply/card_{card_index}_elements.txt', 'w', encoding='utf-8') as f:
                    f.write("CARD TEXT:\n")
                    f.write(card.text + "\n\n")
                    
                    f.write("BUTTONS:\n")
                    buttons = card.find_elements(By.TAG_NAME, "button")
                    for i, btn in enumerate(buttons):
                        try:
                            f.write(f"Button {i+1}: Text='{btn.text}', Class='{btn.get_attribute('class')}', Displayed={btn.is_displayed()}\n")
                        except:
                            f.write(f"Button {i+1}: [Error extracting details]\n")
                    
                    f.write("\nLINKS:\n")
                    links = card.find_elements(By.TAG_NAME, "a")
                    for i, link in enumerate(links):
                        try:
                            f.write(f"Link {i+1}: Text='{link.text}', Class='{link.get_attribute('class')}', Displayed={link.is_displayed()}\n")
                        except:
                            f.write(f"Link {i+1}: [Error extracting details]\n")
                    
                    f.write("\nSHADOW DOM ELEMENTS:\n")
                    shadow_hosts = card.find_elements(By.CSS_SELECTOR, "*")
                    shadow_count = 0
                    for host in shadow_hosts:
                        try:
                            has_shadow = self.driver.execute_script("return arguments[0].shadowRoot !== null", host)
                            if has_shadow:
                                shadow_count += 1
                                f.write(f"Shadow host {shadow_count}: Tag='{host.tag_name}', Class='{host.get_attribute('class')}'\n")
                        except:
                            continue
            except:
                pass
            
            self.logger.info("No Easy Apply option found for this job")
            return False
            
        except Exception as e:
            self.logger.warning(f"Error checking Easy Apply availability: {str(e)}")
            return False
    
    def extract_job_details(self, card) -> Optional[Tuple[Dict, str]]:
        """Extract job details from card and detailed view"""
        original_window = self.driver.current_window_handle
        
        try:
            # Basic details from card with more robust extraction
            job_details = {
                'title': 'Unknown Job',
                'company': 'Unknown Company',
                'location': 'Unknown Location'
            }
            
            # Try to get title
            for selector in ["[data-cy='card-title-link']", ".card-title-link", "a.job-title", "h2 a", "h3 a"]:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    if title_elem:
                        job_details['title'] = title_elem.text
                        break
                except:
                    continue
            
            # Try to get company
            for selector in ["[data-cy='search-result-company-name']", ".company-name", ".employer", "[data-cy='company-name']"]:
                try:
                    company_elem = card.find_element(By.CSS_SELECTOR, selector)
                    if company_elem:
                        job_details['company'] = company_elem.text
                        break
                except:
                    continue
            
            # Try to get location
            for selector in ["[data-cy='search-result-location']", ".location", ".job-location"]:
                try:
                    location_elem = card.find_element(By.CSS_SELECTOR, selector)
                    if location_elem:
                        job_details['location'] = location_elem.text
                        break
                except:
                    continue
            
            # Find and click the title link to open job details
            title_link = None
            for selector in ["[data-cy='card-title-link']", ".card-title-link", "a.job-title", "h2 a", "h3 a"]:
                try:
                    title_link = card.find_element(By.CSS_SELECTOR, selector)
                    if title_link:
                        break
                except:
                    continue
            
            if not title_link:
                self.logger.error("Could not find job title link to click")
                return None
            
            job_details['url'] = title_link.get_attribute('href') or ''
            
            # Scroll the element into view before clicking
            self.driver.execute_script("arguments[0].scrollIntoView(true);", title_link)
            time.sleep(1)  # Give a moment for the scroll to complete
            
            # Try multiple click methods
            clicked = False
            try:
                title_link.click()
                clicked = True
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", title_link)
                    clicked = True
                except Exception as e:
                    self.logger.error(f"Could not click job title link: {str(e)}")
                    return None
            
            if not clicked:
                return None
            
            self.random_delay('between_actions')
            
            # Switch to new window with timeout
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.window_handles) > 1
                )
                
                new_window = None
                for window in self.driver.window_handles:
                    if window != original_window:
                        new_window = window
                        break
                
                if new_window:
                    self.driver.switch_to.window(new_window)
                else:
                    self.logger.error("New window was not created")
                    return None
            except:
                self.logger.error("Timeout waiting for new window")
                return None
            
            # Wait for job details page to load
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except:
                self.logger.warning("Timeout waiting for page to load completely")
            
            # Extract skills with multiple methods
            skills = []
            
            # Method 1: Try to find a dedicated skills section
            skill_selectors = [
                "[data-cy='skillsList']",
                ".skills-list",
                ".job-skills",
                "[data-automation='skills']"
            ]
            
            for selector in skill_selectors:
                try:
                    skills_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # Try different ways to extract skills
                    skill_item_selectors = [
                        "span[id^='skillChip']",
                        ".skill-item",
                        "li",
                        "span.skill"
                    ]
                    
                    for item_selector in skill_item_selectors:
                        try:
                            skill_items = skills_element.find_elements(
                                By.CSS_SELECTOR, item_selector
                            )
                            if skill_items:
                                skills = [skill.text for skill in skill_items if skill.text.strip()]
                                break
                        except:
                            continue
                    
                    if skills:
                        break
                except:
                    continue
            
            # Method 2: If we couldn't find skills using selectors, try extracting from description
            if not skills:
                try:
                    # Look for common patterns in job descriptions
                    description_text = ''
                    for selector in ["#jobDescription", ".job-description", "[data-cy='description']"]:
                        try:
                            desc_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if desc_elem:
                                description_text = desc_elem.text
                                break
                        except:
                            continue
                    
                    if description_text:
                        # Try to find skills section
                        skills_section = None
                        for pattern in ["Skills:", "Requirements:", "Qualifications:", "Required Skills:"]:
                            if pattern in description_text:
                                parts = description_text.split(pattern, 1)
                                if len(parts) > 1:
                                    skills_section = parts[1]
                                    break
                        
                        if skills_section:
                            # Extract skills from the section
                            lines = skills_section.split('\n')
                            skill_candidates = []
                            
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                    
                                # Stop at next heading
                                if line.endswith(':') and len(line) < 50:
                                    break
                                    
                                # Check for bullet points
                                if line.startswith(('•', '-', '*', '·')) or (len(line) < 50 and ',' not in line):
                                    skill_candidates.append(line.lstrip('•-*· '))
                            
                            if skill_candidates:
                                skills = skill_candidates[:10]  # Limit to 10 skills
                except Exception as e:
                    self.logger.warning(f"Error extracting skills from description: {str(e)}")
            
            # Extract description with multiple selectors
            description = "No description available"
            for selector in ["#jobDescription", ".job-description", "[data-cy='description']", "div[class*='description']"]:
                try:
                    desc_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if desc_elem:
                        description = desc_elem.text
                        if description.strip():
                            break
                except:
                    continue
            
            job_details['skills'] = skills or ["Not specified"]
            job_details['description'] = description
            
            # Generate unique job ID from content
            content = f"{job_details['title']}{job_details['company']}{job_details['description'][:100]}"
            job_details['job_id'] = hashlib.md5(content.encode()).hexdigest()
            
            # Save job details
            job_file = JOBS_DIR / f"{job_details['job_id']}.json"
            with open(job_file, 'w', encoding='utf-8') as f:
                json.dump(job_details, f, indent=2)
            
            # Important: Don't close the window - we need it for applying!
            return job_details, original_window
            
        except Exception as e:
            self.logger.error(f"Error extracting job details: {str(e)}")
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(original_window)
            return None

    def is_already_applied(self, card) -> bool:
        """Check if already applied to job with shadow DOM support"""
        try:
            # Method 1: Check for visible "Applied" indicators in the UI
            applied_indicators = [
                ".ribbon-status-applied",
                ".search-status-ribbon-mobile.ribbon-status-applied",
                ".status-applied",
                ".already-applied"
            ]
            
            for indicator in applied_indicators:
                if card.find_elements(By.CSS_SELECTOR, indicator):
                    self.logger.info(f"Found applied indicator: {indicator}")
                    return True
            
            # Method 2: Check for apply-button-wc web component
            apply_buttons = card.find_elements(By.TAG_NAME, "apply-button-wc")
            if apply_buttons:
                for apply_button in apply_buttons:
                    # Get the job ID for logging
                    job_id = apply_button.get_attribute('job-id')
                    
                    # Use JavaScript to check if this job is already applied
                    # This will look inside the shadow DOM for "Application Submitted" text
                    is_applied = self.driver.execute_script("""
                        const applyButton = arguments[0];
                        
                        // Access the shadow root
                        if (!applyButton.shadowRoot) return false;
                        
                        // Look for application-submitted component
                        const appSubmitted = applyButton.shadowRoot.querySelector('application-submitted');
                        if (appSubmitted) return true;
                        
                        // If no application-submitted, check for any text indicating application status
                        const shadowText = applyButton.shadowRoot.textContent.toLowerCase();
                        return shadowText.includes('application submitted') || 
                            shadowText.includes('applied') ||
                            shadowText.includes('app submitted');
                    """, apply_button)
                    
                    if is_applied:
                        self.logger.info(f"Found applied status in shadow DOM for job ID: {job_id}")
                        return True
            
            # Method 3: Check for any text in the card indicating already applied
            try:
                card_text = card.text.lower()
                applied_texts = ['application submitted', 'applied', 'app submitted']
                
                for text in applied_texts:
                    if text in card_text:
                        self.logger.info(f"Found applied text indicator: '{text}'")
                        return True
            except:
                pass
            
            # Method 4: Check if job ID is in our tracked applications
            job_id = self.get_job_id_from_card(card)
            if job_id and self.tracker.is_job_applied(job_id):
                self.logger.info(f"Found job ID {job_id} in tracker as already applied")
                return True
                    
            return False
            
        except Exception as e:
            self.logger.warning(f"Error checking applied status: {str(e)}")
            # Default to false on error - better to try to apply again than to skip incorrectly
            return False
    

    def wait_for_element_with_retry(self, by, selector, timeout=15, retries=2):
        """Wait for element with retries"""
        for attempt in range(retries + 1):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, selector))
                )
                return element
            except (TimeoutException, StaleElementReferenceException):
                if attempt < retries:
                    self.logger.warning(f"Retry {attempt + 1} waiting for element: {selector}")
                    time.sleep(2)
                else:
                    return None
        return None

    def click_easy_apply(self) -> bool:
        """Click the Easy Apply button with improved shadow DOM support"""
        try:
            self.logger.info("Attempting to find and click Easy Apply button")
            
            # Create debug directory
            debug_dir = Path('debug/easy_apply_click')
            debug_dir.mkdir(parents=True, exist_ok=True)
            
            # Take a screenshot before attempting to click
            try:
                self.driver.save_screenshot(f'debug/easy_apply_click/before_click_{self.jobs_processed}.png')
            except:
                pass
            
            # Save page HTML for debugging
            try:
                page_html = self.driver.page_source
                with open(f'debug/easy_apply_click/page_{self.jobs_processed}.html', 'w', encoding='utf-8') as f:
                    f.write(page_html)
            except:
                pass
            
            # Method 1: Look for apply-button-wc web component
            apply_buttons = self.driver.find_elements(By.TAG_NAME, "apply-button-wc")
            if apply_buttons:
                for apply_button in apply_buttons:
                    self.logger.info("Found apply-button-wc web component")
                    
                    # Check first if it's already applied
                    is_applied = self.driver.execute_script("""
                        const applyButton = arguments[0];
                        
                        // Access the shadow root
                        if (!applyButton.shadowRoot) return false;
                        
                        // Look for application-submitted component
                        const appSubmitted = applyButton.shadowRoot.querySelector('application-submitted');
                        if (appSubmitted) return true;
                        
                        // Check for any text indicating application status
                        const shadowText = applyButton.shadowRoot.textContent.toLowerCase();
                        return shadowText.includes('application submitted') || 
                            shadowText.includes('applied') ||
                            shadowText.includes('app submitted');
                    """, apply_button)
                    
                    if is_applied:
                        self.logger.info("Job already applied according to shadow DOM")
                        return False
                    
                    # Get a screenshot of the web component
                    try:
                        apply_button.screenshot(f'debug/easy_apply_click/button_wc_{self.jobs_processed}.png')
                    except:
                        pass
                    
                    # Try to click the button inside shadow DOM
                    clicked = self.driver.execute_script("""
                        const applyButton = arguments[0];
                        
                        // Access the shadow root
                        if (!applyButton.shadowRoot) return false;
                        
                        // Look for any clickable elements
                        const clickCandidates = [
                            applyButton.shadowRoot.querySelector('button'),
                            applyButton.shadowRoot.querySelector('a[role="button"]'),
                            applyButton.shadowRoot.querySelector('[class*="apply"]'),
                            applyButton.shadowRoot.querySelector('[class*="button"]'),
                            applyButton.shadowRoot.querySelector('div[role="button"]')
                        ].filter(el => el !== null);
                        
                        // Try to click the first available clickable element
                        for (const elem of clickCandidates) {
                            try {
                                // Add visual indicator for debugging
                                elem.style.border = '3px solid red';
                                setTimeout(() => {
                                    elem.click();
                                }, 500);
                                return true;
                            } catch (e) {
                                console.error('Error clicking in shadow DOM:', e);
                            }
                        }
                        
                        return false;
                    """, apply_button)
                    
                    if clicked:
                        self.logger.info("Clicked button in shadow DOM")
                        time.sleep(2)
                        
                        # Take screenshot after click
                        try:
                            self.driver.save_screenshot(f'debug/easy_apply_click/after_shadow_click_{self.jobs_processed}.png')
                        except:
                            pass
                        
                        # Check if application form appeared
                        form_selectors = [
                            ".apply-container", 
                            ".application-form", 
                            "form[data-cy='applicationForm']",
                            ".resume-container",
                            ".cover-letter-container"
                        ]
                        
                        for selector in form_selectors:
                            try:
                                form = self.driver.find_element(By.CSS_SELECTOR, selector)
                                if form.is_displayed():
                                    self.logger.info(f"Application form appeared: {selector}")
                                    return True
                            except:
                                continue
                        
                        # If we didn't find a form, wait a bit longer and check again
                        time.sleep(3)
                        for selector in form_selectors:
                            try:
                                form = self.driver.find_element(By.CSS_SELECTOR, selector)
                                if form.is_displayed():
                                    self.logger.info(f"Application form appeared after delay: {selector}")
                                    return True
                            except:
                                continue
                        
                        # Since we know we clicked something in the shadow DOM,
                        # let's return true even if we didn't detect a form yet
                        return True
            
            # Method 2: Standard button selectors
            button_selectors = [
                "[data-cy='easyApplyBtn']",
                ".easy-apply-button",
                "button.easy-apply",
                "a.easy-apply",
                "button[class*='easyApply']",
                "button[class*='easy-apply']",
                "a[class*='easyApply']",
                "a[class*='easy-apply']",
                "button.job-app",
                "button.apply-button",
                "a.apply-button"
            ]
            
            for selector in button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        for button in buttons:
                            # Check if it's visible and enabled
                            if button.is_displayed() and button.is_enabled():
                                self.logger.info(f"Found Easy Apply button with selector: {selector}")
                                
                                # Scroll into view
                                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                                time.sleep(1)
                                
                                # Try clicking
                                if self.click_with_retry(button, retries=5):
                                    # Take screenshot after click
                                    try:
                                        self.driver.save_screenshot(f'debug/easy_apply_click/after_click_{self.jobs_processed}.png')
                                    except:
                                        pass
                                    
                                    return True
                except Exception as e:
                    self.logger.warning(f"Error with selector {selector}: {str(e)}")
                    continue
            
            # Method 3: Look for any button with "Apply" text
            try:
                apply_elements = self.driver.find_elements(
                    By.XPATH, 
                    "//button[contains(translate(text(), 'APPLY', 'apply'), 'apply')] | //a[contains(translate(text(), 'APPLY', 'apply'), 'apply')]"
                )
                
                for element in apply_elements:
                    if element.is_displayed() and element.is_enabled():
                        self.logger.info(f"Found button with Apply text: {element.text}")
                        
                        # Scroll into view
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        time.sleep(1)
                        
                        # Try clicking
                        if self.click_with_retry(element, retries=5):
                            # Take screenshot after click
                            try:
                                self.driver.save_screenshot(f'debug/easy_apply_click/after_text_click_{self.jobs_processed}.png')
                            except:
                                pass
                            
                            return True
            except Exception as e:
                self.logger.warning(f"Error with text-based search: {str(e)}")
            
            # Method 4: Last resort - try to find any apply-related elements with JavaScript
            try:
                # Save all available buttons and links for debugging
                buttons_and_links = self.driver.find_elements(By.CSS_SELECTOR, "button, a")
                with open(f'debug/easy_apply_click/all_buttons_{self.jobs_processed}.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Found {len(buttons_and_links)} buttons and links\n\n")
                    
                    for i, element in enumerate(buttons_and_links):
                        try:
                            text = element.text
                            is_displayed = element.is_displayed()
                            is_enabled = element.is_enabled()
                            
                            f.write(f"Element {i+1}:\n")
                            f.write(f"  Tag: {element.tag_name}\n")
                            f.write(f"  Text: '{text}'\n")
                            f.write(f"  Class: '{element.get_attribute('class')}'\n")
                            f.write(f"  ID: '{element.get_attribute('id')}'\n")
                            f.write(f"  Displayed: {is_displayed}\n")
                            f.write(f"  Enabled: {is_enabled}\n\n")
                        except:
                            f.write(f"Element {i+1}: [Error extracting details]\n\n")
                
                # Try JavaScript-based approach
                clicked = self.driver.execute_script("""
                    // Find any apply-related elements
                    const elements = Array.from(document.querySelectorAll('*')).filter(el => {
                        // Check if it's visible
                        const rect = el.getBoundingClientRect();
                        const isVisible = rect.width > 0 && rect.height > 0;
                        
                        if (!isVisible) return false;
                        
                        // Check text content
                        const text = (el.textContent || '').toLowerCase();
                        if (text.includes('apply') && !text.includes('applied')) return true;
                        
                        // Check classes
                        const className = (el.className || '').toLowerCase();
                        if (className.includes('apply') || className.includes('button')) return true;
                        
                        // Check IDs
                        const id = (el.id || '').toLowerCase();
                        if (id.includes('apply') || id.includes('button')) return true;
                        
                        return false;
                    });
                    
                    // Try to click the first applicable element
                    for (const el of elements) {
                        try {
                            // Highlight for debugging
                            el.style.border = '3px solid red';
                            
                            // Wait a bit and click
                            setTimeout(() => {
                                el.click();
                            }, 500);
                            
                            return true;
                        } catch (e) {
                            console.error('Error clicking element:', e);
                        }
                    }
                    
                    return false;
                """)
                
                if clicked:
                    self.logger.info("Clicked apply element using JavaScript")
                    time.sleep(2)
                    
                    # Take screenshot after click
                    try:
                        self.driver.save_screenshot(f'debug/easy_apply_click/after_js_click_{self.jobs_processed}.png')
                    except:
                        pass
                    
                    # Since we used JavaScript to click, let's assume it worked
                    return True
            except Exception as e:
                self.logger.warning(f"Error with JavaScript approach: {str(e)}")
            
            self.logger.error("Failed to find or click Easy Apply button")
            return False
            
        except Exception as e:
            self.logger.error(f"Error clicking Easy Apply: {str(e)}")
            return False
    
    def analyze_page_structure(self):
        """
        Analyze the current page structure to determine proper selectors
        This diagnostic method helps when the website structure changes
        """
        try:
            self.logger.info("Analyzing page structure...")
            
            # Create debug directory if it doesn't exist
            debug_dir = Path('debug')
            debug_dir.mkdir(parents=True, exist_ok=True)
            
            # Take screenshot of current page
            self.driver.save_screenshot('debug/page_screenshot.png')
            
            # Get page source and save it
            page_source = self.driver.page_source
            with open('debug/page_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
                
            # Log URL
            with open('debug/current_url.txt', 'w') as f:
                f.write(self.driver.current_url)
            
            # Check for job cards container
            containers = [
                "div[id='searchDisplay-div']",
                ".job-search-results",
                ".jobs-list",
                "dhi-search-results",
                "div[class*='search-results']"
            ]
            
            container_element = None
            for container in containers:
                try:
                    container_element = self.driver.find_element(By.CSS_SELECTOR, container)
                    if container_element:
                        self.logger.info(f"Found job container with selector: {container}")
                        break
                except NoSuchElementException:
                    continue
            
            if not container_element:
                self.logger.warning("Could not find job container - website structure may have changed")
                
                # Save all div elements with their classes for analysis
                divs = self.driver.find_elements(By.TAG_NAME, "div")
                with open('debug/all_divs.txt', 'w', encoding='utf-8') as f:
                    for i, div in enumerate(divs):
                        try:
                            class_name = div.get_attribute('class')
                            id_name = div.get_attribute('id')
                            f.write(f"Div {i+1}:\n")
                            f.write(f"  Class: {class_name}\n")
                            f.write(f"  ID: {id_name}\n\n")
                        except:
                            pass
                
                return False
            
            # Check for job card elements
            card_selectors = [
                "dhi-search-card[data-cy='search-card']",
                ".search-card",
                ".job-card",
                ".job-listing",
                "div[class*='card']",
                "div[class*='job']"
            ]
            
            job_cards = []
            cards_selector_used = None
            for selector in card_selectors:
                try:
                    cards = container_element.find_elements(By.CSS_SELECTOR, selector)
                    if cards and len(cards) > 0:
                        self.logger.info(f"Found {len(cards)} job cards with selector: {selector}")
                        job_cards = cards
                        cards_selector_used = selector
                        break
                except:
                    continue
            
            if not job_cards:
                self.logger.warning("Could not find job cards - website structure may have changed")
                return False
            
            # If we found cards, analyze the first one in detail
            if job_cards and len(job_cards) > 0:
                first_card = job_cards[0]
                
                # Save screenshot of the first card
                try:
                    first_card.screenshot('debug/first_card.png')
                except:
                    self.logger.warning("Could not take screenshot of first card")
                
                # Save HTML of the first card
                try:
                    card_html = first_card.get_attribute('outerHTML')
                    with open('debug/first_card.html', 'w', encoding='utf-8') as f:
                        f.write(card_html)
                except Exception as e:
                    self.logger.warning(f"Could not save first card HTML: {str(e)}")
                
                # Check available selectors within the card
                with open('debug/card_selectors.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Job Card Selector: {cards_selector_used}\n\n")
                    
                    # Check for job title
                    for selector in ["[data-cy='card-title-link']", ".card-title-link", "a.job-title", "h2 a", "h3 a"]:
                        try:
                            elements = first_card.find_elements(By.CSS_SELECTOR, selector)
                            f.write(f"Title selector '{selector}': {len(elements)} elements found\n")
                            if elements:
                                for i, elem in enumerate(elements):
                                    f.write(f"  Element {i+1} text: {elem.text}\n")
                                    f.write(f"  Element {i+1} href: {elem.get_attribute('href')}\n")
                        except Exception as e:
                            f.write(f"Title selector '{selector}': Error - {str(e)}\n")
                    
                    f.write("\n")
                    
                    # Check for company name
                    for selector in ["[data-cy='search-result-company-name']", ".company-name", ".employer"]:
                        try:
                            elements = first_card.find_elements(By.CSS_SELECTOR, selector)
                            f.write(f"Company selector '{selector}': {len(elements)} elements found\n")
                            if elements:
                                for i, elem in enumerate(elements):
                                    f.write(f"  Element {i+1} text: {elem.text}\n")
                        except Exception as e:
                            f.write(f"Company selector '{selector}': Error - {str(e)}\n")
                    
                    f.write("\n")
                    
                    # Check for Easy Apply
                    for selector in ["[data-cy='easyApplyBtn']", ".easy-apply-button", ".easy-apply"]:
                        try:
                            elements = first_card.find_elements(By.CSS_SELECTOR, selector)
                            f.write(f"Easy Apply selector '{selector}': {len(elements)} elements found\n")
                            if elements:
                                for i, elem in enumerate(elements):
                                    f.write(f"  Element {i+1} text: {elem.text}\n")
                        except Exception as e:
                            f.write(f"Easy Apply selector '{selector}': Error - {str(e)}\n")
                    
                    f.write("\n")
                    
                    # Check for web component apply button
                    try:
                        web_components = first_card.find_elements(By.TAG_NAME, "apply-button-wc")
                        f.write(f"Web Component 'apply-button-wc': {len(web_components)} elements found\n")
                    except Exception as e:
                        f.write(f"Web Component 'apply-button-wc': Error - {str(e)}\n")
                    
                    f.write("\n")
                    
                    # Find all buttons in the card
                    try:
                        buttons = first_card.find_elements(By.TAG_NAME, "button")
                        f.write(f"Buttons: {len(buttons)} elements found\n")
                        if buttons:
                            for i, button in enumerate(buttons):
                                f.write(f"  Button {i+1} text: {button.text}\n")
                                f.write(f"  Button {i+1} class: {button.get_attribute('class')}\n")
                                f.write(f"  Button {i+1} id: {button.get_attribute('id')}\n")
                    except Exception as e:
                        f.write(f"Buttons: Error - {str(e)}\n")
                    
                    f.write("\n")
                    
                    # Find all links in the card
                    try:
                        links = first_card.find_elements(By.TAG_NAME, "a")
                        f.write(f"Links: {len(links)} elements found\n")
                        if links:
                            for i, link in enumerate(links):
                                f.write(f"  Link {i+1} text: {link.text}\n")
                                f.write(f"  Link {i+1} href: {link.get_attribute('href')}\n")
                                f.write(f"  Link {i+1} class: {link.get_attribute('class')}\n")
                    except Exception as e:
                        f.write(f"Links: Error - {str(e)}\n")
            
            self.logger.info("Page structure analysis complete. Debug data saved to 'debug' directory.")
            return True
            
        except Exception as e:
            self.logger.error(f"Error analyzing page structure: {str(e)}")
            return False
    def submit_application(self, job_details: Dict) -> bool:
        """Submit job application"""
        try:
            self.logger.info(f"Generating optimized resume for {job_details['title']}")
            # Generate optimized resume
            resume_path = self.resume_handler.generate_resume(job_details)
            if not resume_path:
                self.logger.error("Failed to generate resume")
                # Record failed application in tracker
                self.tracker.add_application(
                    job_details, 
                    'failed',
                    notes="Failed to generate resume"
                )
                return False
                
            self.logger.info("Generating cover letter")
            # Generate cover letter
            cover_letter = self.gemini.generate_cover_letter(
                job_details,
                resume_path
            )
            
            cover_letter_path = None
            if cover_letter:
                # Create a professional filename for the cover letter
                # Get the base resume filename (without path or extension)
                resume_filename = os.path.basename(resume_path)
                base_name = os.path.splitext(resume_filename)[0]
                
                # Replace "Resume" with "Cover_Letter" in the filename
                cover_letter_base = base_name.replace("Resume", "Cover_Letter")
                
                # Ensure the filename is unique
                cover_letter_filename = self._ensure_unique_filename(cover_letter_base, ".txt")
                
                # Save to RESUME_DIR to keep documents together
                cover_letter_path = RESUME_DIR / cover_letter_filename
                
                with open(cover_letter_path, 'w') as f:
                    f.write(cover_letter)
                self.logger.info(f"Cover letter saved to {cover_letter_path}")
            else:
                self.logger.warning("No cover letter generated")
            
            self.logger.info("Clicking Easy Apply button")
            # Click Easy Apply
            if not self.click_easy_apply():
                self.logger.error("Failed to click Easy Apply button")
                # Record failed application in tracker
                self.tracker.add_application(
                    job_details, 
                    'failed',
                    resume_path,
                    cover_letter_path,
                    notes="Failed to click Easy Apply button"
                )
                return False
                
            self.random_delay('between_actions')
            
            # Wait for the application container to be visible
            self.logger.info("Waiting for application form")
            application_container = self.wait_for_element_with_retry(
                By.CSS_SELECTOR, 
                ".apply-container",
                timeout=20,
                retries=3
            )
            
            if not application_container:
                self.logger.error("Application form not found")
                # Record failed application in tracker
                self.tracker.add_application(
                    job_details, 
                    'failed',
                    resume_path,
                    cover_letter_path,
                    notes="Application form not found"
                )
                return False
                
            # Check if existing resume is already selected or need to upload new one
            self.logger.info("Checking resume status")
            time.sleep(3)  # Give the form time to fully load
            
            # Look for file upload element
            try:
                # First check if we need to upload a resume or if one is already selected
                resume_container = self.wait_for_element_with_retry(
                    By.CSS_SELECTOR,
                    ".resume-container",
                    timeout=5
                )
                
                if resume_container:
                    # Check if there's a file already selected
                    existing_file = resume_container.find_elements(By.CSS_SELECTOR, ".file-wrapper")
                    
                    if existing_file:
                        self.logger.info("Existing resume found, replacing it")
                        # Click replace button
                        replace_button = resume_container.find_element(
                            By.CSS_SELECTOR,
                            ".file-remove"
                        )
                        if not self.click_with_retry(replace_button):
                            self.logger.warning("Could not click replace button, trying to continue")
                    else:
                        self.logger.info("No existing resume found, uploading new one")
                        # Look for direct file input
                        file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                        if file_inputs:
                            file_inputs[0].send_keys(str(resume_path))
                        else:
                            self.logger.error("No file input found for resume")
                            # Record failed application in tracker
                            self.tracker.add_application(
                                job_details, 
                                'failed',
                                resume_path,
                                cover_letter_path,
                                notes="No file input found for resume"
                            )
                            return False
                else:
                    self.logger.warning("Resume container not found, looking for file input")
                    # Look for direct file input
                    file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                    if file_inputs:
                        file_inputs[0].send_keys(str(resume_path))
                    else:
                        self.logger.error("No file input found for resume")
                        # Record failed application in tracker
                        self.tracker.add_application(
                            job_details, 
                            'failed',
                            resume_path,
                            cover_letter_path,
                            notes="No file input found for resume"
                        )
                        return False
            except Exception as e:
                self.logger.error(f"Error handling resume upload: {str(e)}")
                
            # Wait for file picker if it appeared
            time.sleep(3)
            try:
                # Check if file picker modal appeared
                file_picker = self.driver.find_elements(By.CSS_SELECTOR, ".fsp-modal__body")
                if file_picker:
                    self.logger.info("File picker modal appeared, handling it")
                    # Find file input in modal
                    file_input = self.driver.find_element(By.CSS_SELECTOR, "#fsp-fileUpload")
                    file_input.send_keys(str(resume_path))
                    
                    # Wait for file to upload and click next/upload button
                    time.sleep(2)
                    upload_buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, 
                        ".fsp-button.fsp-button--primary:not(.fsp-button--disabled)"
                    )
                    if upload_buttons:
                        self.click_with_retry(upload_buttons[0])
                        time.sleep(2)
                    
                    # Look for final upload button if needed
                    final_upload = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        ".fsp-button-upload"
                    )
                    if final_upload:
                        self.click_with_retry(final_upload[0])
                        time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Error handling file picker: {str(e)}")
                
            # Upload cover letter if available
            if cover_letter_path:
                try:
                    self.logger.info("Uploading cover letter")
                    # Look for cover letter button
                    cover_letter_buttons = self.driver.find_elements(
                        By.CSS_SELECTOR, 
                        ".file-picker-wrapper.cover-letter button"
                    )
                    
                    if cover_letter_buttons:
                        self.logger.info("Found cover letter upload button")
                        self.click_with_retry(cover_letter_buttons[0])
                        
                        # Wait for file picker to appear
                        time.sleep(2)
                        try:
                            # Check if file picker modal appeared
                            file_picker = self.driver.find_elements(By.CSS_SELECTOR, ".fsp-modal__body")
                            if file_picker:
                                self.logger.info("File picker modal appeared for cover letter")
                                # Find file input in modal
                                file_input = self.driver.find_element(By.CSS_SELECTOR, "#fsp-fileUpload")
                                file_input.send_keys(str(cover_letter_path))
                                
                                # Wait for file to upload and click next/upload button
                                time.sleep(2)
                                upload_buttons = self.driver.find_elements(
                                    By.CSS_SELECTOR, 
                                    ".fsp-button.fsp-button--primary:not(.fsp-button--disabled)"
                                )
                                if upload_buttons:
                                    self.click_with_retry(upload_buttons[0])
                                    time.sleep(2)
                                
                                # Look for final upload button
                                final_upload = self.driver.find_elements(
                                    By.CSS_SELECTOR,
                                    ".fsp-button-upload"
                                )
                                if final_upload:
                                    self.click_with_retry(final_upload[0])
                                    time.sleep(2)
                        except Exception as e:
                            self.logger.warning(f"Error handling cover letter file picker: {str(e)}")
                    else:
                        self.logger.warning("No cover letter upload button found")
                except Exception as e:
                    self.logger.warning(f"Could not upload cover letter: {str(e)}")
            
            # Click through application steps
            self.logger.info("Clicking through application steps")
            
            # Initial next button on first page
            try:
                next_button = self.wait_for_element_with_retry(
                    By.CSS_SELECTOR,
                    ".navigation-buttons .btn-next",
                    timeout=10
                )
                
                if next_button and self.click_with_retry(next_button):
                    self.logger.info("Clicked Next button")
                    self.random_delay('between_actions')
                else:
                    self.logger.warning("Could not find or click Next button")
            except Exception as e:
                self.logger.warning(f"Error clicking Next button: {str(e)}")
                
            # Submit button on review page
            try:
                submit_button = self.wait_for_element_with_retry(
                    By.CSS_SELECTOR,
                    ".navigation-buttons .btn-next",
                    timeout=10
                )
                
                if submit_button and self.click_with_retry(submit_button):
                    self.logger.info("Clicked Submit button")
                    self.random_delay('between_actions')
                else:
                    self.logger.warning("Could not find or click Submit button")
            except Exception as e:
                self.logger.warning(f"Error clicking Submit button: {str(e)}")
            
            # Verify success
            try:
                success = self.wait_for_element_with_retry(
                    By.CSS_SELECTOR,
                    ".post-apply-banner",
                    timeout=15,
                    retries=3
                )
                
                if success:
                    self.logger.info("Application submitted successfully")
                    
                    # Add applied date to job details
                    job_file = JOBS_DIR / f"{job_details['job_id']}.json"
                    if job_file.exists():
                        try:
                            with open(job_file, 'r') as f:
                                job_data = json.load(f)
                            
                            job_data['applied_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            job_data['resume_file'] = os.path.basename(resume_path)
                            if cover_letter_path:
                                job_data['cover_letter_file'] = os.path.basename(cover_letter_path)
                            
                            with open(job_file, 'w') as f:
                                json.dump(job_data, f, indent=2)
                        except Exception as e:
                            self.logger.warning(f"Error updating job details with application info: {str(e)}")
                    
                    # Record successful application in tracker
                    self.tracker.add_application(
                        job_details, 
                        'success',
                        resume_path,
                        cover_letter_path
                    )
                    
                    self.jobs_applied += 1
                    return True
                else:
                    self.logger.warning("No success banner found")
                    # Record failed application in tracker
                    self.tracker.add_application(
                        job_details, 
                        'failed',
                        resume_path,
                        cover_letter_path,
                        notes="No success banner found"
                    )
                    return False
            except Exception as e:
                self.logger.warning(f"Error verifying application success: {str(e)}")
                # Record failed application in tracker
                self.tracker.add_application(
                    job_details, 
                    'failed',
                    resume_path,
                    cover_letter_path,
                    notes=f"Error verifying application success: {str(e)}"
                )
                return False
            
        except Exception as e:
            self.logger.error(f"Error submitting application: {str(e)}")
            # Record failed application in tracker
            self.tracker.add_application(
                job_details, 
                'failed',
                notes=f"Error submitting application: {str(e)}"
            )
            return False

    def _ensure_unique_filename(self, base_filename: str, extension: str) -> str:
        """Ensure filename is unique by adding a counter if needed"""
        filename = f"{base_filename}{extension}"
        counter = 1
        
        while (RESUME_DIR / filename).exists():
            # Add version number for better tracking
            filename = f"{base_filename}_v{counter}{extension}"
            counter += 1
            
        return filename

    def click_with_retry(self, element, retries=3) -> bool:
        """Click element with retries"""
        for attempt in range(retries + 1):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                element.click()
                return True
            except Exception:
                try:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )
                    return True
                except Exception as e:
                    if attempt < retries:
                        self.logger.warning(f"Retry {attempt + 1} clicking element: {str(e)}")
                        self.random_delay('between_actions')
                    else:
                        self.logger.error(f"Failed to click element after {retries} retries")
                        return False
        return False

    def process_search_results(self) -> int:
        """Process all jobs on current page, returns number of new jobs found"""
        new_jobs_found = 0
        try:
            # Find all job cards with multiple selectors
            job_cards = []
            selectors = [
                "dhi-search-card[data-cy='search-card']",
                ".search-card",
                ".job-card",
                ".job-listing",
                "div[class*='card']",
                "div[class*='job']"
            ]
            
            for selector in selectors:
                try:
                    cards = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, selector)
                        )
                    )
                    if cards and len(cards) > 0:
                        job_cards = cards
                        self.logger.info(f"Found {len(cards)} job cards with selector: {selector}")
                        break
                except:
                    continue
            
            if not job_cards:
                self.logger.error("No job cards found on current page")
                return new_jobs_found
            
            self.logger.info(f"Found {len(job_cards)} job cards")
            
            # Create debug directory if it doesn't exist
            debug_dir = Path('debug/cards')
            debug_dir.mkdir(parents=True, exist_ok=True)
            
            for index, card in enumerate(job_cards):
                self.jobs_processed += 1
                self.tracker.increment_jobs_found()
                new_jobs_found += 1
                
                # Take a screenshot of the card for debugging
                try:
                    card.screenshot(f'debug/cards/card_{self.jobs_processed}.png')
                except:
                    pass
                
                # Optimized flow: First check if already applied
                is_applied = False
                try:
                    is_applied = self.is_already_applied(card)
                except Exception as e:
                    self.logger.warning(f"Error checking if already applied: {str(e)}")
                
                if is_applied:
                    self.logger.info("Skipping already applied job")
                    self.jobs_skipped += 1
                    continue
                
                # Then check if Easy Apply is available
                has_easy_apply = False
                try:
                    has_easy_apply = self.check_easy_apply_available(card)
                except Exception as e:
                    self.logger.warning(f"Error checking Easy Apply availability: {str(e)}")
                
                if not has_easy_apply:
                    self.logger.info("Skipping job without Easy Apply")
                    
                    # Try to get basic job info to record the skip
                    try:
                        # Try multiple selectors for job title and company
                        title = "Unknown"
                        company = "Unknown"
                        location = "Unknown"
                        job_id = f"unknown_{self.jobs_processed}"
                        
                        # Try to get title
                        for selector in ["[data-cy='card-title-link']", ".card-title-link", "a.job-title", "h2", "h3"]:
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, selector)
                                if title_elem:
                                    title = title_elem.text
                                    break
                            except:
                                continue
                        
                        # Try to get company
                        for selector in ["[data-cy='search-result-company-name']", ".company-name", ".employer", "[data-cy='company-name']"]:
                            try:
                                company_elem = card.find_element(By.CSS_SELECTOR, selector)
                                if company_elem:
                                    company = company_elem.text
                                    break
                            except:
                                continue
                        
                        # Try to get location
                        for selector in ["[data-cy='search-result-location']", ".location", ".job-location"]:
                            try:
                                location_elem = card.find_element(By.CSS_SELECTOR, selector)
                                if location_elem:
                                    location = location_elem.text
                                    break
                            except:
                                continue
                        
                        # Try to get job ID
                        try:
                            job_id = self.get_job_id_from_card(card) or job_id
                        except:
                            pass
                        
                        job_info = {
                            'job_id': job_id,
                            'title': title,
                            'company': company,
                            'location': location
                        }
                        
                        # Save HTML structure of the card for debugging
                        try:
                            with open(f'debug/cards/card_{self.jobs_processed}_html.txt', 'w', encoding='utf-8') as f:
                                f.write(card.get_attribute('outerHTML'))
                        except:
                            pass
                        
                        # Record skipped application in tracker
                        self.tracker.add_application(
                            job_info, 
                            'skipped',
                            notes="No Easy Apply available"
                        )
                    except Exception as e:
                        self.logger.warning(f"Error recording skipped job: {str(e)}")
                    
                    self.jobs_skipped += 1
                    continue
                
                # Now we only process jobs that are not applied and have Easy Apply
                # Extract job details and keep window open
                try:
                    result = self.extract_job_details(card)
                    if not result:
                        self.jobs_skipped += 1
                        continue
                        
                    job_details, original_window = result
                    
                    # Submit application while on the detail page
                    application_result = self.submit_application(job_details)
                    
                    if application_result:
                        self.logger.info(
                            f"Successfully applied to {job_details['title']}"
                        )
                    else:
                        self.logger.warning(
                            f"Failed to apply to {job_details['title']}"
                        )
                    
                    # Now close the detail window and return to search results
                    self.logger.info("Closing job detail window")
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(original_window)
                        
                    self.random_delay('between_applications')
                except Exception as e:
                    self.logger.error(f"Error processing job: {str(e)}")
                    # Make sure we're back to the search window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
            
            return new_jobs_found
                
        except Exception as e:
            self.logger.error(f"Error processing search results: {str(e)}")
            return new_jobs_found

    def next_page_exists(self) -> bool:
        """Check if next page exists"""
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR,
                "li.pagination-next:not(.disabled)"
            )
            return bool(next_button)
        except:
            return False

    def go_to_next_page(self) -> bool:
        """Go to next page of results"""
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR,
                "li.pagination-next:not(.disabled) a"
            )
            if self.click_with_retry(next_button):
                self.random_delay('page_load')
                return True
            return False
        except:
            return False

    def search_jobs(self, title: str) -> bool:
        """Search for jobs with given title"""
        try:
            search_url = DICE_SEARCH_URL.format(quote(title))
            self.driver.get(search_url)
            self.random_delay('page_load')
            
             # Add this line to analyze the page structure
            self.analyze_page_structure()

            # Verify search results loaded
            results = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[id='searchDisplay-div']")
                )
            )
            return bool(results)
            
        except Exception as e:
            self.logger.error(f"Error searching jobs: {str(e)}")
            return False

    def generate_summary_report(self):
        """Generate and print summary of the session"""
        report = self.tracker.generate_report()
        
        # Add session-specific stats
        session_report = [
            "",
            "Current Session Stats:",
            f"- Jobs processed: {self.jobs_processed}",
            f"- Jobs applied: {self.jobs_applied}",
            f"- Jobs skipped: {self.jobs_skipped}",
            f"- Success rate: {(self.jobs_applied / max(1, self.jobs_processed)) * 100:.1f}%",
            ""
        ]
        
        full_report = report + "\n" + "\n".join(session_report)
        
        # Print to console
        print("\n" + full_report)
        
        # Save to file
        report_dir = Path('reports')
        report_dir.mkdir(exist_ok=True)
        
        report_path = report_dir / f'application_report_{datetime.now():%Y%m%d_%H%M%S}.txt'
        with open(report_path, 'w') as f:
            f.write(full_report)
            
        return report_path

    def run(self):
        """Main execution flow"""
        try:
             # Create debug directory
            debug_dir = Path('debug')
            debug_dir.mkdir(exist_ok=True)
            
            if not self.setup_driver():
                return
                
            # Randomize job titles
            random.shuffle(JOB_TITLES)
            
            for title in JOB_TITLES:
                self.logger.info(f"Processing job title: {title}")
                
                if not self.search_jobs(title):
                    continue
                    
                page = 1
                total_new_jobs = 0
                
                while True:
                    self.logger.info(f"Processing page {page}")
                    new_jobs = self.process_search_results()
                    total_new_jobs += new_jobs
                    
                    self.logger.info(f"Found {new_jobs} new jobs on page {page}")
                    
                    if not self.next_page_exists():
                        break
                        
                    if not self.go_to_next_page():
                        break
                        
                    page += 1
                    self.random_delay('between_pages')
                
                self.logger.info(f"Total new jobs found for '{title}': {total_new_jobs}")
                self.random_delay('between_actions')
                
            # Generate summary report
            report_path = self.generate_summary_report()
            self.logger.info(f"Session report saved to: {report_path}")
                
        except Exception as e:
            self.logger.error(f"Error in main execution: {str(e)}")
            
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")