"""
Supabase Storage Service for uploading and managing profile pictures
"""

import os
from supabase import create_client, Client
from typing import Optional, Dict

class SupabaseStorageService:
    """Supabase Storage service for profile picture operations"""

    def __init__(self):
        """Initialize Supabase Storage service"""
        self.client: Optional[Client] = None
        self.bucket_name = 'profile-pictures'
        self._initialize_service()

    def _initialize_service(self):
        """Initialize the Supabase client"""
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY')

            if not supabase_url or not supabase_key:
                print("[WARNING] Supabase credentials not found. Profile pictures will be stored locally.")
                return

            self.client = create_client(supabase_url, supabase_key)
            print("[SUCCESS] Supabase Storage service initialized successfully")

        except Exception as e:
            print(f"[ERROR] Failed to initialize Supabase Storage service: {e}")
            self.client = None

    def upload_file(self, file_data: bytes, filename: str, content_type: str = 'image/jpeg') -> Dict:
        """
        Upload a file to Supabase Storage

        Args:
            file_data: File data as bytes
            filename: Name for the file
            content_type: MIME type of the file

        Returns:
            dict: {'success': bool, 'public_url': str, 'path': str, 'error': str}
        """
        if not self.client:
            return {
                'success': False,
                'error': 'Supabase Storage service not initialized'
            }

        try:
            # Upload file to Supabase Storage
            response = self.client.storage.from_(self.bucket_name).upload(
                path=filename,
                file=file_data,
                file_options={
                    'content-type': content_type,
                    'cache-control': '3600',
                    'upsert': 'true'  # Replace if file already exists
                }
            )

            # Get public URL for the uploaded file
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(filename)

            return {
                'success': True,
                'public_url': public_url,
                'path': filename
            }

        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Failed to upload file to Supabase Storage: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from Supabase Storage

        Args:
            filename: Name of the file to delete

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            self.client.storage.from_(self.bucket_name).remove([filename])
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete file from Supabase Storage: {e}")
            return False

    def get_filename_from_url(self, url: str) -> Optional[str]:
        """
        Extract filename from Supabase Storage URL

        Args:
            url: Supabase Storage URL

        Returns:
            str: Filename or None
        """
        try:
            if 'supabase' in url and self.bucket_name in url:
                # Extract filename from URL like:
                # https://project.supabase.co/storage/v1/object/public/profile-pictures/filename.png
                parts = url.split(f'{self.bucket_name}/')
                if len(parts) > 1:
                    return parts[1].split('?')[0]  # Remove query params if any
            return None
        except Exception:
            return None

    def is_available(self) -> bool:
        """Check if Supabase Storage service is available"""
        return self.client is not None

    def check_bucket_exists(self) -> bool:
        """Check if the profile-pictures bucket exists"""
        if not self.client:
            return False

        try:
            buckets = self.client.storage.list_buckets()
            return any(bucket.name == self.bucket_name for bucket in buckets)
        except Exception as e:
            print(f"[ERROR] Failed to check bucket existence: {e}")
            return False

    def create_bucket(self) -> bool:
        """
        Create the profile-pictures bucket if it doesn't exist

        Returns:
            bool: True if bucket exists or was created successfully
        """
        if not self.client:
            return False

        try:
            # Check if bucket already exists
            if self.check_bucket_exists():
                print(f"[INFO] Bucket '{self.bucket_name}' already exists")
                return True

            # Create the bucket
            self.client.storage.create_bucket(
                self.bucket_name,
                options={
                    'public': True,  # Make bucket public
                    'file_size_limit': 5242880,  # 5MB limit
                    'allowed_mime_types': ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
                }
            )
            print(f"[SUCCESS] Created bucket '{self.bucket_name}'")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to create bucket: {e}")
            return False


# Singleton instance
_storage_service = None

def get_storage_service():
    """Get or create SupabaseStorageService instance"""
    global _storage_service
    if _storage_service is None:
        _storage_service = SupabaseStorageService()
    return _storage_service
