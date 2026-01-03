"""
Google Drive Service for uploading and managing files
"""

import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

class GoogleDriveService:
    """Google Drive service for file operations"""

    def __init__(self):
        """Initialize Google Drive service"""
        self.service = None
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self._initialize_service()

    def _initialize_service(self):
        """Initialize the Google Drive API service"""
        try:
            # Load credentials from environment variable or file
            credentials_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')

            if credentials_json:
                # If credentials are stored as JSON string in environment
                credentials_info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
            else:
                # If credentials are in a file
                credentials_file = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE', 'credentials.json')
                if os.path.exists(credentials_file):
                    credentials = service_account.Credentials.from_service_account_file(
                        credentials_file,
                        scopes=['https://www.googleapis.com/auth/drive.file']
                    )
                else:
                    print("[WARNING] Google Drive credentials not found. Profile pictures will be stored locally.")
                    return

            self.service = build('drive', 'v3', credentials=credentials)
            print("[SUCCESS] Google Drive service initialized successfully")

        except Exception as e:
            print(f"[ERROR] Failed to initialize Google Drive service: {e}")
            self.service = None

    def upload_file(self, file_data, filename, mimetype='image/jpeg'):
        """
        Upload a file to Google Drive

        Args:
            file_data: File data (bytes or file object)
            filename: Name for the file
            mimetype: MIME type of the file

        Returns:
            dict: {'success': bool, 'file_id': str, 'web_view_link': str, 'direct_link': str}
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Google Drive service not initialized'
            }

        try:
            # Prepare file metadata
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id] if self.folder_id else []
            }

            # Convert file_data to BytesIO if it's bytes
            if isinstance(file_data, bytes):
                file_data = io.BytesIO(file_data)

            # Upload file
            media = MediaIoBaseUpload(file_data, mimetype=mimetype, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink, webContentLink'
            ).execute()

            file_id = file.get('id')

            # Make the file publicly accessible
            self.service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()

            # Get direct download link
            direct_link = f"https://drive.google.com/uc?export=view&id={file_id}"

            return {
                'success': True,
                'file_id': file_id,
                'web_view_link': file.get('webViewLink'),
                'direct_link': direct_link
            }

        except HttpError as error:
            print(f"[ERROR] Google Drive API error: {error}")
            return {
                'success': False,
                'error': f'Google Drive API error: {error}'
            }
        except Exception as e:
            print(f"[ERROR] Failed to upload file: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def delete_file(self, file_id):
        """
        Delete a file from Google Drive

        Args:
            file_id: Google Drive file ID

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            return False

        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete file: {e}")
            return False

    def get_file_id_from_url(self, url):
        """
        Extract file ID from Google Drive URL

        Args:
            url: Google Drive URL

        Returns:
            str: File ID or None
        """
        try:
            if 'drive.google.com' in url:
                if 'id=' in url:
                    return url.split('id=')[1].split('&')[0]
                elif '/d/' in url:
                    return url.split('/d/')[1].split('/')[0]
            return None
        except Exception:
            return None

    def is_available(self):
        """Check if Google Drive service is available"""
        return self.service is not None


# Singleton instance
_drive_service = None

def get_drive_service():
    """Get or create GoogleDriveService instance"""
    global _drive_service
    if _drive_service is None:
        _drive_service = GoogleDriveService()
    return _drive_service
