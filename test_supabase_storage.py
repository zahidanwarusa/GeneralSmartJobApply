#!/usr/bin/env python3
"""
Test script for Supabase Storage integration
Run this to verify your Supabase Storage setup is working correctly
"""

import sys
import os

# Add webapp to path
sys.path.insert(0, 'webapp')

from services.supabase_storage import get_storage_service
from dotenv import load_dotenv

# Load environment variables
load_dotenv('webapp/.env')

def test_service_initialization():
    """Test if Supabase Storage service initializes correctly"""
    print("=" * 70)
    print("Supabase Storage Integration Test")
    print("=" * 70)
    print()

    print("[1/5] Testing service initialization...")
    storage_service = get_storage_service()

    if storage_service.is_available():
        print("   \u2713 Supabase Storage service initialized successfully")
        return storage_service
    else:
        print("   \u2717 Supabase Storage service not available")
        print()
        print("   Possible reasons:")
        print("   - SUPABASE_URL not set in .env")
        print("   - SUPABASE_ANON_KEY not set in .env")
        print("   - Invalid Supabase credentials")
        print()
        print("   Check your .env file and try again")
        return None

def test_configuration():
    """Test if configuration is correct"""
    print("\n[2/5] Checking configuration...")

    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if supabase_url:
        print(f"   SUPABASE_URL: \u2713 {supabase_url}")
    else:
        print("   SUPABASE_URL: \u2717 Not set")

    if supabase_key:
        print(f"   SUPABASE_ANON_KEY: \u2713 Set (hidden)")
    else:
        print("   SUPABASE_ANON_KEY: \u2717 Not set")

def test_bucket_exists():
    """Test if profile-pictures bucket exists"""
    print("\n[3/5] Checking if 'profile-pictures' bucket exists...")

    storage_service = get_storage_service()
    if not storage_service.is_available():
        print("   \u2717 Skipping (service not available)")
        return False

    try:
        exists = storage_service.check_bucket_exists()
        if exists:
            print("   \u2713 Bucket 'profile-pictures' exists")
            return True
        else:
            print("   \u2717 Bucket 'profile-pictures' does not exist")
            print()
            print("   To create the bucket:")
            print("   1. Go to https://supabase.com/dashboard")
            print("   2. Select your project")
            print("   3. Click 'Storage' in sidebar")
            print("   4. Click 'New bucket'")
            print("   5. Name: profile-pictures")
            print("   6. Public: Check this box")
            print("   7. Click 'Create bucket'")
            return False
    except Exception as e:
        print(f"   \u2717 Error checking bucket: {e}")
        return False

def test_upload():
    """Test uploading a file"""
    print("\n[4/5] Testing file upload...")

    storage_service = get_storage_service()
    if not storage_service.is_available():
        print("   \u2717 Skipping upload test (service not available)")
        return None

    # Create a simple test image (1x1 pixel PNG)
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    try:
        print("   Uploading test image...")
        result = storage_service.upload_file(
            test_image,
            'test_profile_picture.png',
            'image/png'
        )

        if result['success']:
            print(f"   \u2713 Upload successful!")
            print(f"   Public URL: {result['public_url']}")
            return result['path']
        else:
            print(f"   \u2717 Upload failed: {result.get('error', 'Unknown error')}")
            print()
            print("   Common causes:")
            print("   - Bucket doesn't exist")
            print("   - Bucket policies not configured")
            print("   - Network issues")
            return None

    except Exception as e:
        print(f"   \u2717 Upload error: {e}")
        return None

def test_delete(filename):
    """Test deleting a file"""
    if not filename:
        print("\n[5/5] Skipping delete test (no file to delete)")
        return

    print("\n[5/5] Testing file deletion...")

    storage_service = get_storage_service()

    try:
        print(f"   Deleting test file ({filename})...")
        success = storage_service.delete_file(filename)

        if success:
            print("   \u2713 File deleted successfully")
        else:
            print("   \u2717 Failed to delete file")
            print(f"   You may need to manually delete it from Supabase Dashboard")

    except Exception as e:
        print(f"   \u2717 Delete error: {e}")

def print_summary(service_available, bucket_exists, filename):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    if service_available and bucket_exists and filename:
        print("\u2713 All tests passed!")
        print()
        print("Your Supabase Storage integration is working correctly.")
        print("You can now upload profile pictures in the SmartApply dashboard.")
        print()
        print("Next steps:")
        print("1. Go to http://localhost:5000/dashboard/user/profile")
        print("2. Upload a profile picture")
        print("3. Check your Supabase Dashboard to see the uploaded file")
    elif service_available and bucket_exists:
        print("\u26a0 Partial success")
        print()
        print("Supabase Storage is configured, but upload/delete failed.")
        print("Please check:")
        print("- Bucket policies allow INSERT/UPDATE/DELETE for authenticated users")
        print("- Bucket allows public SELECT")
        print("- Network connection is stable")
    elif service_available:
        print("\u26a0 Partial success")
        print()
        print("Supabase Storage service is available, but bucket not found.")
        print()
        print("To fix:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Click 'Storage' → 'New bucket'")
        print("4. Name: profile-pictures")
        print("5. Public: Check this box")
        print("6. Create bucket and configure policies")
        print()
        print("See SUPABASE_STORAGE_SETUP.md for detailed instructions")
    else:
        print("\u2717 Tests failed")
        print()
        print("Supabase Storage integration is not configured.")
        print()
        print("To set up Supabase Storage:")
        print("1. Follow the guide in SUPABASE_STORAGE_SETUP.md")
        print("2. Ensure SUPABASE_URL and SUPABASE_ANON_KEY are in .env")
        print("3. Create 'profile-pictures' bucket in Supabase Dashboard")
        print()
        print("The application will fall back to local storage until configured.")

    print()

def main():
    """Run all tests"""
    storage_service = test_service_initialization()
    service_available = storage_service is not None

    test_configuration()

    bucket_exists = False
    if service_available:
        bucket_exists = test_bucket_exists()

    filename = None
    if service_available and bucket_exists:
        filename = test_upload()
        if filename:
            test_delete(filename)

    print_summary(service_available, bucket_exists, filename)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\u2717 Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n\u2717 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
