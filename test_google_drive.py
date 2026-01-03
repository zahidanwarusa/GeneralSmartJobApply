#!/usr/bin/env python3
"""
Test script for Google Drive integration
Run this to verify your Google Drive setup is working correctly
"""

import sys
import os

# Add webapp to path
sys.path.insert(0, 'webapp')

from services.google_drive import get_drive_service
from dotenv import load_dotenv

# Load environment variables
load_dotenv('webapp/.env')

def test_service_initialization():
    """Test if Google Drive service initializes correctly"""
    print("=" * 70)
    print("Google Drive Integration Test")
    print("=" * 70)
    print()

    print("[1/4] Testing service initialization...")
    drive_service = get_drive_service()

    if drive_service.is_available():
        print("   ✓ Google Drive service initialized successfully")
        return drive_service
    else:
        print("   ✗ Google Drive service not available")
        print()
        print("   Possible reasons:")
        print("   - Credentials file not found or invalid")
        print("   - Environment variables not set correctly")
        print("   - Google Drive API not enabled")
        print()
        print("   Run setup_google_drive.py to configure Google Drive")
        return None

def test_configuration():
    """Test if configuration is correct"""
    print("\n[2/4] Checking configuration...")

    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')
    creds_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')

    print(f"   GOOGLE_DRIVE_FOLDER_ID: {folder_id if folder_id else '✗ Not set'}")

    if creds_json:
        print(f"   GOOGLE_DRIVE_CREDENTIALS: ✓ Set (JSON string)")
    elif creds_file:
        if os.path.exists(creds_file):
            print(f"   GOOGLE_DRIVE_CREDENTIALS_FILE: ✓ {creds_file} (exists)")
        else:
            print(f"   GOOGLE_DRIVE_CREDENTIALS_FILE: ✗ {creds_file} (not found)")
    else:
        print("   Credentials: ✗ Not set")

def test_upload():
    """Test uploading a file"""
    print("\n[3/4] Testing file upload...")

    drive_service = get_drive_service()
    if not drive_service.is_available():
        print("   ✗ Skipping upload test (service not available)")
        return

    # Create a simple test image (1x1 pixel PNG)
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    try:
        print("   Uploading test image...")
        result = drive_service.upload_file(
            test_image,
            'test_profile_picture.png',
            'image/png'
        )

        if result['success']:
            print(f"   ✓ Upload successful!")
            print(f"   File ID: {result['file_id']}")
            print(f"   Direct Link: {result['direct_link']}")
            return result['file_id']
        else:
            print(f"   ✗ Upload failed: {result.get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"   ✗ Upload error: {e}")
        return None

def test_delete(file_id):
    """Test deleting a file"""
    if not file_id:
        print("\n[4/4] Skipping delete test (no file to delete)")
        return

    print("\n[4/4] Testing file deletion...")

    drive_service = get_drive_service()

    try:
        print(f"   Deleting test file (ID: {file_id})...")
        success = drive_service.delete_file(file_id)

        if success:
            print("   ✓ File deleted successfully")
        else:
            print("   ✗ Failed to delete file")
            print(f"   You may need to manually delete it from Google Drive")

    except Exception as e:
        print(f"   ✗ Delete error: {e}")

def print_summary(service_available, file_id):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    if service_available and file_id:
        print("✓ All tests passed!")
        print()
        print("Your Google Drive integration is working correctly.")
        print("You can now upload profile pictures in the SmartApply dashboard.")
    elif service_available:
        print("⚠ Partial success")
        print()
        print("Google Drive service is available, but upload/delete failed.")
        print("Please check:")
        print("- Service account has Editor access to the folder")
        print("- Folder ID is correct")
        print("- Google Drive API is enabled")
    else:
        print("✗ Tests failed")
        print()
        print("Google Drive integration is not configured.")
        print()
        print("To set up Google Drive:")
        print("1. Follow the guide in GOOGLE_DRIVE_SETUP.md")
        print("2. Or run: python setup_google_drive.py")
        print()
        print("The application will fall back to local storage until configured.")

    print()

def main():
    """Run all tests"""
    drive_service = test_service_initialization()
    service_available = drive_service is not None

    test_configuration()

    file_id = None
    if service_available:
        file_id = test_upload()
        if file_id:
            test_delete(file_id)

    print_summary(service_available, file_id)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
