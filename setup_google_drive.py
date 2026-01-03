#!/usr/bin/env python3
"""
Google Drive Setup Helper Script
This script helps you set up Google Drive integration for profile pictures.
"""

import os
import json
import sys

def print_header():
    print("=" * 70)
    print("Google Drive Setup Helper for SmartApply")
    print("=" * 70)
    print()

def check_credentials_file():
    """Check if credentials file exists"""
    print("[1/4] Checking for Google Drive credentials file...")

    credentials_files = [
        'google-drive-credentials.json',
        'credentials.json',
        'service-account-credentials.json'
    ]

    for filename in credentials_files:
        if os.path.exists(filename):
            print(f"   ✓ Found credentials file: {filename}")
            return filename

    print("   ✗ No credentials file found")
    print()
    print("   Please download your service account credentials from:")
    print("   https://console.cloud.google.com/apis/credentials")
    print()
    print("   Save the JSON file as: google-drive-credentials.json")
    print("   in the project root directory")
    return None

def validate_credentials(filename):
    """Validate credentials file format"""
    print(f"\n[2/4] Validating credentials file: {filename}...")

    try:
        with open(filename, 'r') as f:
            creds = json.load(f)

        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds]

        if missing_fields:
            print(f"   ✗ Missing fields in credentials: {', '.join(missing_fields)}")
            return None

        if creds['type'] != 'service_account':
            print(f"   ✗ Invalid credential type: {creds['type']}")
            print("   Expected: service_account")
            return None

        print("   ✓ Credentials file is valid")
        print(f"   Service Account Email: {creds['client_email']}")
        return creds

    except json.JSONDecodeError:
        print("   ✗ Invalid JSON format in credentials file")
        return None
    except Exception as e:
        print(f"   ✗ Error reading credentials: {e}")
        return None

def get_folder_id():
    """Prompt user for Google Drive folder ID"""
    print("\n[3/4] Google Drive Folder Configuration...")
    print()
    print("   Create a folder in Google Drive for profile pictures:")
    print("   1. Go to https://drive.google.com/")
    print("   2. Create a new folder (e.g., 'SmartApply Profile Pictures')")
    print("   3. Share the folder with your service account email")
    print("   4. Give it 'Editor' permissions")
    print("   5. Copy the folder ID from the URL")
    print()
    print("   Folder URL format:")
    print("   https://drive.google.com/drive/folders/FOLDER_ID_HERE")
    print("                                         ↑ Copy this part")
    print()

    folder_id = input("   Enter your Google Drive Folder ID: ").strip()

    if not folder_id:
        print("   ✗ Folder ID cannot be empty")
        return None

    print(f"   ✓ Folder ID: {folder_id}")
    return folder_id

def update_env_file(credentials_filename, folder_id):
    """Update .env file with Google Drive configuration"""
    print("\n[4/4] Updating .env file...")

    env_path = os.path.join('webapp', '.env')

    # Check if .env exists
    if not os.path.exists(env_path):
        print(f"   Creating new .env file at: {env_path}")
        # Copy from .env.example if it exists
        example_path = os.path.join('webapp', '.env.example')
        if os.path.exists(example_path):
            with open(example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)

    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Remove existing Google Drive config
    lines = [line for line in lines if not line.startswith('GOOGLE_DRIVE_')]

    # Add new Google Drive config
    if not lines[-1].endswith('\n'):
        lines.append('\n')

    lines.append('\n# Google Drive Configuration (Auto-generated)\n')
    lines.append(f'GOOGLE_DRIVE_FOLDER_ID={folder_id}\n')
    lines.append(f'GOOGLE_DRIVE_CREDENTIALS_FILE={credentials_filename}\n')

    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(lines)

    print(f"   ✓ Updated {env_path}")
    print(f"   Added GOOGLE_DRIVE_FOLDER_ID={folder_id}")
    print(f"   Added GOOGLE_DRIVE_CREDENTIALS_FILE={credentials_filename}")

def print_success():
    """Print success message with next steps"""
    print("\n" + "=" * 70)
    print("✓ Google Drive setup completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Make sure you've shared the Google Drive folder with the service account")
    print("2. Restart your Flask application")
    print("3. Navigate to Profile page and upload a picture")
    print("4. Check your Google Drive folder to verify the upload")
    print()
    print("For troubleshooting, see: GOOGLE_DRIVE_SETUP.md")
    print()

def main():
    """Main setup function"""
    print_header()

    # Step 1: Check for credentials file
    credentials_filename = check_credentials_file()
    if not credentials_filename:
        print("\n✗ Setup failed: No credentials file found")
        sys.exit(1)

    # Step 2: Validate credentials
    credentials = validate_credentials(credentials_filename)
    if not credentials:
        print("\n✗ Setup failed: Invalid credentials file")
        sys.exit(1)

    # Step 3: Get folder ID
    folder_id = get_folder_id()
    if not folder_id:
        print("\n✗ Setup failed: Invalid folder ID")
        sys.exit(1)

    # Step 4: Update .env file
    try:
        update_env_file(credentials_filename, folder_id)
    except Exception as e:
        print(f"\n✗ Setup failed: Error updating .env file: {e}")
        sys.exit(1)

    # Success!
    print_success()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        sys.exit(1)
