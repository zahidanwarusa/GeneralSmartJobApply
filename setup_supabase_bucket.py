#!/usr/bin/env python3
"""
Automatic Supabase Storage Bucket Setup
This script creates the profile-pictures bucket automatically
"""

import sys
import os

# Add webapp to path
sys.path.insert(0, 'webapp')

from dotenv import load_dotenv
load_dotenv('webapp/.env')

from supabase import create_client

def setup_bucket():
    print("=" * 70)
    print("Supabase Storage Bucket Setup")
    print("=" * 70)
    print()

    # Get credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_ANON_KEY')

    if not supabase_url or not supabase_key:
        print("[ERROR] Supabase credentials not found in .env file")
        print()
        print("Please ensure you have:")
        print("  SUPABASE_URL=your-supabase-url")
        print("  SUPABASE_ANON_KEY=your-anon-key")
        print()
        return False

    print(f"[1/3] Connecting to Supabase...")
    print(f"      URL: {supabase_url}")

    try:
        client = create_client(supabase_url, supabase_key)
        print("      [SUCCESS] Connected to Supabase")
    except Exception as e:
        print(f"      [ERROR] Failed to connect: {e}")
        return False

    print()
    print("[2/3] Checking if 'profile-pictures' bucket exists...")

    try:
        buckets = client.storage.list_buckets()
        bucket_exists = any(bucket.name == 'profile-pictures' for bucket in buckets)

        if bucket_exists:
            print("      [INFO] Bucket 'profile-pictures' already exists")
            print()
            print("Your bucket is ready to use!")
            return True
    except Exception as e:
        print(f"      [WARNING] Could not check buckets: {e}")

    print()
    print("[3/3] Creating 'profile-pictures' bucket...")

    try:
        # Create the bucket
        client.storage.create_bucket(
            'profile-pictures',
            options={
                'public': True,
                'file_size_limit': 5242880,  # 5MB
                'allowed_mime_types': ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
            }
        )
        print("      [SUCCESS] Created bucket 'profile-pictures'")
        print()
        print("=" * 70)
        print("Setup Complete!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. The bucket is now ready to use")
        print("2. Go to your Supabase Dashboard and configure bucket policies:")
        print("   - Go to: https://supabase.com/dashboard")
        print("   - Select your project")
        print("   - Click 'Storage' -> 'profile-pictures' bucket")
        print("   - Click 'Policies' tab")
        print("   - Add these policies:")
        print()
        print("   Policy 1: Public Read Access")
        print("   - Template: 'Enable read access for all users'")
        print("   - This allows anyone to view profile pictures")
        print()
        print("   Policy 2: Authenticated Upload")
        print("   - Template: 'Enable insert for authenticated users only'")
        print("   - This allows logged-in users to upload pictures")
        print()
        print("   Policy 3: Authenticated Update")
        print("   - Template: 'Enable update for authenticated users'")
        print("   - This allows users to update their pictures")
        print()
        print("   Policy 4: Authenticated Delete")
        print("   - Template: 'Enable delete for authenticated users'")
        print("   - This allows cleanup of old pictures")
        print()
        print("3. Test by uploading a profile picture in your app")
        print()
        return True

    except Exception as e:
        print(f"      [ERROR] Failed to create bucket: {e}")
        print()
        print("Manual Setup Required:")
        print("1. Go to: https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Click 'Storage' in the sidebar")
        print("4. Click 'New bucket'")
        print("5. Enter these settings:")
        print("   - Name: profile-pictures")
        print("   - Public bucket: YES (check the box)")
        print("   - File size limit: 5 MB")
        print("6. Click 'Create bucket'")
        print("7. Configure policies (see above for details)")
        print()
        return False

if __name__ == '__main__':
    try:
        success = setup_bucket()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
