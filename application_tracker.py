import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ApplicationTracker:
    """Tracks job applications and manages application statistics"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.tracking_file = base_dir / 'tracking' / 'applications.csv'
        self.stats_file = base_dir / 'tracking' / 'statistics.json'
        
        # Create tracking directory if it doesn't exist
        tracking_dir = base_dir / 'tracking'
        tracking_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tracking file if it doesn't exist
        if not self.tracking_file.exists():
            with open(self.tracking_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'job_id', 
                    'title', 
                    'company', 
                    'location',
                    'applied_date', 
                    'resume_file', 
                    'cover_letter_file',
                    'status',
                    'notes'
                ])
        
        # Initialize stats file if it doesn't exist
        if not self.stats_file.exists():
            stats = {
                'total_jobs_found': 0,
                'total_applications': 0,
                'successful_applications': 0,
                'failed_applications': 0,
                'skipped_applications': 0,
                'daily_stats': {},
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
    
    def add_application(self, job_details: Dict, status: str, resume_file: Optional[str] = None, 
                        cover_letter_file: Optional[str] = None, notes: str = '') -> None:
        """Add a new application to the tracking file"""
        with open(self.tracking_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                job_details.get('job_id', ''),
                job_details.get('title', ''),
                job_details.get('company', ''),
                job_details.get('location', ''),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.path.basename(resume_file) if resume_file else '',
                os.path.basename(cover_letter_file) if cover_letter_file else '',
                status,
                notes
            ])
        
        # Update statistics
        self._update_statistics(status)
    
    def is_job_applied(self, job_id: str) -> bool:
        """Check if a job has already been applied to"""
        if not self.tracking_file.exists():
            return False
            
        with open(self.tracking_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0] == job_id:
                    return True
        return False
    
    def get_application_stats(self) -> Dict:
        """Get application statistics"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_recent_applications(self, limit: int = 10) -> List[Dict]:
        """Get the most recent applications"""
        applications = []
        if not self.tracking_file.exists():
            return applications
            
        with open(self.tracking_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                applications.append(dict(row))
                if len(applications) >= limit:
                    break
        
        return applications
    
    def get_daily_stats(self, date: Optional[str] = None) -> Dict:
        """Get stats for a specific day (YYYY-MM-DD format)"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        stats = self.get_application_stats()
        daily_stats = stats.get('daily_stats', {})
        
        return daily_stats.get(date, {
            'jobs_found': 0,
            'applications': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        })
    
    def _update_statistics(self, status: str) -> None:
        """Update the statistics file with new application data"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                'total_jobs_found': 0,
                'total_applications': 0,
                'successful_applications': 0,
                'failed_applications': 0,
                'skipped_applications': 0,
                'daily_stats': {},
                'last_updated': ''
            }
        
        # Update total counts
        stats['total_applications'] += 1
        
        if status == 'success':
            stats['successful_applications'] += 1
        elif status == 'failed':
            stats['failed_applications'] += 1
        elif status == 'skipped':
            stats['skipped_applications'] += 1
        
        # Update daily stats
        if today not in stats['daily_stats']:
            stats['daily_stats'][today] = {
                'jobs_found': 0,
                'applications': 0,
                'successful': 0,
                'failed': 0,
                'skipped': 0
            }
        
        stats['daily_stats'][today]['applications'] += 1
        
        if status == 'success':
            stats['daily_stats'][today]['successful'] += 1
        elif status == 'failed':
            stats['daily_stats'][today]['failed'] += 1
        elif status == 'skipped':
            stats['daily_stats'][today]['skipped'] += 1
        
        stats['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def increment_jobs_found(self) -> None:
        """Increment the count of jobs found"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                'total_jobs_found': 0,
                'total_applications': 0,
                'successful_applications': 0,
                'failed_applications': 0,
                'skipped_applications': 0,
                'daily_stats': {},
                'last_updated': ''
            }
        
        # Update total jobs found
        stats['total_jobs_found'] += 1
        
        # Update daily stats
        if today not in stats['daily_stats']:
            stats['daily_stats'][today] = {
                'jobs_found': 0,
                'applications': 0,
                'successful': 0,
                'failed': 0,
                'skipped': 0
            }
        
        stats['daily_stats'][today]['jobs_found'] += 1
        stats['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate a detailed report of application activities"""
        stats = self.get_application_stats()
        today_stats = self.get_daily_stats()
        
        report = []
        report.append("=======================================")
        report.append("SmartApplyPro Application Activity Report")
        report.append("=======================================")
        report.append("")
        report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("Overall Statistics:")
        report.append(f"- Total jobs found: {stats.get('total_jobs_found', 0)}")
        report.append(f"- Total applications: {stats.get('total_applications', 0)}")
        report.append(f"- Successful applications: {stats.get('successful_applications', 0)}")
        report.append(f"- Failed applications: {stats.get('failed_applications', 0)}")
        report.append(f"- Skipped applications: {stats.get('skipped_applications', 0)}")
        report.append("")
        report.append("Today's Activity:")
        report.append(f"- Jobs found: {today_stats.get('jobs_found', 0)}")
        report.append(f"- Applications: {today_stats.get('applications', 0)}")
        report.append(f"- Successful: {today_stats.get('successful', 0)}")
        report.append(f"- Failed: {today_stats.get('failed', 0)}")
        report.append(f"- Skipped: {today_stats.get('skipped', 0)}")
        report.append("")
        
        # Recent applications
        recent = self.get_recent_applications(5)
        if recent:
            report.append("Recent Applications:")
            for app in recent:
                report.append(f"- {app.get('applied_date', '')}: {app.get('title', '')} at {app.get('company', '')} - {app.get('status', '')}")
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
        
        return report_text