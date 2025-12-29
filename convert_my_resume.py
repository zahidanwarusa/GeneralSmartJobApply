"""
Simple Resume Converter - Easy-to-use wrapper

This script makes it super easy to convert your resume to JSON format.

USAGE OPTIONS:

1. Text file (paste resume):
   - Open input_your_resume.txt
   - Paste your resume text
   - Run: python convert_my_resume.py

2. Existing file:
   - Run: python convert_my_resume.py --file resume.pdf
   - Run: python convert_my_resume.py --file resume.docx

3. With job optimization:
   - Run: python convert_my_resume.py --optimize --job-file data/jobs/job.json
"""

import sys
import os
import argparse
from pathlib import Path
from resume_converter import ResumeConverter

def print_banner():
    """Print a nice banner"""
    print("\n" + "="*80)
    print("                    RESUME TO JSON CONVERTER")
    print("="*80 + "\n")

def print_success(output_path):
    """Print success message with next steps"""
    print("\n" + "="*80)
    print("[SUCCESS] Your resume has been converted to JSON")
    print("="*80)
    print(f"\nOutput file: {output_path}")
    print("\nNext Steps:")
    print("  1. Review the JSON file:")
    print(f"     notepad {output_path}")
    print("\n  2. Set as default resume:")
    print(f"     copy {output_path} zahid_resume_v2.json")
    print("\n  3. Generate optimized resume for a job:")
    print("     python main.py --mode resume --job-file data/jobs/job.json")
    print("\n  4. Or start automated job applications:")
    print("     python main.py --mode auto")
    print("="*80 + "\n")

def check_input_file():
    """Check if input_your_resume.txt has content"""
    input_file = Path("input_your_resume.txt")

    if not input_file.exists():
        return False, "File 'input_your_resume.txt' not found"

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if it's still the template (contains instruction markers)
    if "PASTE YOUR RESUME BELOW" in content or "[Your Name]" in content:
        return False, "Please paste your actual resume in 'input_your_resume.txt'"

    # Check if there's enough content
    if len(content.strip()) < 100:
        return False, "Resume content seems too short. Please paste your complete resume."

    return True, content

def main():
    """Main conversion workflow"""
    parser = argparse.ArgumentParser(
        description='Convert your resume to JSON format (Easy Mode)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use input_your_resume.txt (paste resume there first)
  python convert_my_resume.py

  # Use existing file
  python convert_my_resume.py --file resume.pdf
  python convert_my_resume.py --file resume.docx

  # With optimization
  python convert_my_resume.py --optimize --job-file data/jobs/job.json
  python convert_my_resume.py --file resume.pdf --optimize --job-file data/jobs/job.json

  # Specify your name
  python convert_my_resume.py --name "John Doe"
        """
    )

    parser.add_argument('--file', '-f', help='Resume file (PDF, DOCX, or TXT). If not provided, uses input_your_resume.txt')
    parser.add_argument('--name', '-n', help='Your name (overrides extracted name)')
    parser.add_argument('--output', '-o', help='Output JSON file path (optional)')
    parser.add_argument('--optimize', action='store_true', help='Optimize resume for job description')
    parser.add_argument('--job-file', '-j', help='Job description JSON file (required if --optimize)')

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Determine input source
    if args.file:
        input_file = args.file
        print(f"[*] Using file: {input_file}")

        if not Path(input_file).exists():
            print(f"\n[ERROR] File not found: {input_file}\n")
            return 1
    else:
        # Use input_your_resume.txt
        print("[*] Using: input_your_resume.txt")

        # Check if file has content
        is_valid, message = check_input_file()
        if not is_valid:
            print(f"\n[ERROR] {message}")
            print("\nHow to use input_your_resume.txt:")
            print("  1. Open: notepad input_your_resume.txt")
            print("  2. Delete the template text")
            print("  3. Paste your complete resume")
            print("  4. Save the file")
            print("  5. Run: python convert_my_resume.py\n")
            return 1

        input_file = "input_your_resume.txt"

    # Validate optimization options
    if args.optimize and not args.job_file:
        print("\n[ERROR] --job-file is required when using --optimize\n")
        return 1

    # Initialize converter
    try:
        print("\n[*] Initializing AI-powered converter...")
        converter = ResumeConverter()

        # Show what we're doing
        print(f"[*] Extracting text from resume...")

        if args.optimize:
            print(f"[*] Optimization enabled for job: {args.job_file}")

        # Convert the resume
        output_path = converter.convert_file(
            input_file=input_file,
            output_file=args.output,
            candidate_name=args.name,
            optimize=args.optimize,
            job_file=args.job_file
        )

        # Success!
        print_success(output_path)

        # Ask if user wants to set as default
        try:
            response = input("Do you want to set this as your default resume? (y/n): ")
            if response.lower() in ['y', 'yes']:
                import shutil
                shutil.copy(output_path, 'zahid_resume_v2.json')
                print("\n[SUCCESS] Set as default resume! SmartApplyPro will now use your resume.\n")
        except:
            pass  # Skip if input not available

        return 0

    except FileNotFoundError as e:
        print(f"\n[ERROR] {str(e)}\n")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Conversion failed: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Make sure your resume has clear sections")
        print("  - Check that all required packages are installed")
        print("  - Try converting again (AI responses can vary)")
        print("  - Review logs above for specific errors\n")
        return 1

if __name__ == '__main__':
    exit(main())
