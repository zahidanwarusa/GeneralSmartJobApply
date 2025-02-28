import argparse
import json
import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from bot import DiceBot
from resume_handler import ResumeHandler
from gemini_service import GeminiService
from application_tracker import ApplicationTracker
from config import JOBS_DIR, RESUME_DIR, DATA_DIR

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_auto_apply():
    """Run automated job application bot"""
    bot = DiceBot()
    bot.run()

def generate_resume(job_description_file: str) -> Optional[str]:
    """Generate optimized resume from job description file"""
    try:
        # Read job description
        with open(job_description_file, 'r') as f:
            job_details = json.load(f)
            
        # Generate resume
        handler = ResumeHandler()
        resume_path = handler.generate_resume(job_details)
        
        if resume_path:
            print(f"\nResume generated successfully: {resume_path}")
            return resume_path
        else:
            print("\nError generating resume")
            return None
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return None

def generate_cover_letter(job_description_file: str, resume_path: str) -> Optional[str]:
    """Generate cover letter from job description and resume"""
    try:
        # Read job description
        with open(job_description_file, 'r') as f:
            job_details = json.load(f)
            
        # Generate cover letter
        gemini = GeminiService()
        cover_letter = gemini.generate_cover_letter(job_details, resume_path)
        
        if cover_letter:
            # Create a professional filename for the cover letter
            # Get the base resume filename (without path or extension)
            resume_filename = os.path.basename(resume_path)
            base_name = os.path.splitext(resume_filename)[0]
            
            # Replace "Resume" with "Cover_Letter" in the filename
            cover_letter_base = base_name.replace("Resume", "Cover_Letter")
            cover_letter_path = RESUME_DIR / f"{cover_letter_base}.txt"
            
            # Check for existing file
            counter = 1
            while cover_letter_path.exists():
                cover_letter_path = RESUME_DIR / f"{cover_letter_base}_v{counter}.txt"
                counter += 1
                
            with open(cover_letter_path, 'w') as f:
                f.write(cover_letter)
                
            print(f"\nCover letter generated successfully: {cover_letter_path}")
            return str(cover_letter_path)
        else:
            print("\nError generating cover letter")
            return None
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return None

def list_applications():
    """List all tracked job applications"""
    try:
        tracker = ApplicationTracker(DATA_DIR)
        
        # Get statistics
        stats = tracker.get_application_stats()
        applications = tracker.get_recent_applications(limit=50)
        
        # Print statistics
        print("\n=======================================")
        print("SmartApplyPro Application Statistics")
        print("=======================================")
        print(f"Total jobs found: {stats.get('total_jobs_found', 0)}")
        print(f"Total applications: {stats.get('total_applications', 0)}")
        print(f"Successful applications: {stats.get('successful_applications', 0)}")
        print(f"Failed applications: {stats.get('failed_applications', 0)}")
        print(f"Skipped applications: {stats.get('skipped_applications', 0)}")
        
        # Get today's stats
        today = datetime.now().strftime("%Y-%m-%d")
        today_stats = stats.get('daily_stats', {}).get(today, {})
        
        print("\nToday's Activity:")
        print(f"Jobs found: {today_stats.get('jobs_found', 0)}")
        print(f"Applications: {today_stats.get('applications', 0)}")
        print(f"Successful: {today_stats.get('successful', 0)}")
        print(f"Failed: {today_stats.get('failed', 0)}")
        print(f"Skipped: {today_stats.get('skipped', 0)}")
        
        # Print recent applications
        if applications:
            print("\nRecent Applications:")
            print("-" * 100)
            print(f"{'Date':<20} {'Status':<10} {'Title':<30} {'Company':<30} {'Resume':<20}")
            print("-" * 100)
            
            for app in applications:
                applied_date = app.get('applied_date', 'Unknown')
                status = app.get('status', 'Unknown')
                title = app.get('title', 'Unknown')[:30]
                company = app.get('company', 'Unknown')[:30]
                resume = app.get('resume_file', 'N/A')[:20]
                
                print(f"{applied_date:<20} {status:<10} {title:<30} {company:<30} {resume:<20}")
            
            print("-" * 100)
        else:
            print("\nNo applications found.")
            
    except Exception as e:
        print(f"\nError listing applications: {str(e)}")

def generate_report():
    """Generate comprehensive application report"""
    try:
        tracker = ApplicationTracker(DATA_DIR)
        report_path = Path('reports') / f'application_report_{datetime.now():%Y%m%d_%H%M%S}.txt'
        
        # Create reports directory if needed
        report_path.parent.mkdir(exist_ok=True)
        
        # Generate the report
        report_text = tracker.generate_report(str(report_path))
        
        print(f"\nReport generated successfully: {report_path}")
        print("\nReport summary:")
        print("-" * 50)
        print(report_text)
        
    except Exception as e:
        print(f"\nError generating report: {str(e)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SmartApplyPro - AI-Powered Job Application Automation System"
    )
    
    parser.add_argument(
        '--mode',
        choices=['auto', 'resume', 'cover', 'list', 'report'],
        default='auto',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--job-file',
        help='Job description JSON file for resume/cover letter generation'
    )
    
    parser.add_argument(
        '--resume',
        help='Resume file for cover letter generation'
    )
    
    args = parser.parse_args()
    
    setup_logging()
    
    if args.mode == 'auto':
        print("\nStarting automated job applications...")
        run_auto_apply()
        
    elif args.mode == 'resume':
        if not args.job_file:
            print("\nError: Job description file required for resume generation")
            return
        generate_resume(args.job_file)
        
    elif args.mode == 'cover':
        if not args.job_file or not args.resume:
            print("\nError: Job file and resume required for cover letter generation")
            return
        generate_cover_letter(args.job_file, args.resume)
        
    elif args.mode == 'list':
        list_applications()
        
    elif args.mode == 'report':
        generate_report()

if __name__ == "__main__":
    main()