# Profile Picture Upload - Quick Start Guide

## Overview

Profile pictures can now be stored in **Google Drive** with automatic fallback to local storage. The system intelligently handles both storage methods.

## How It Works

1. **Google Drive (Preferred)**:
   - Pictures are uploaded to your Google Drive folder
   - Publicly accessible direct links are stored in the database
   - Old pictures are automatically deleted when new ones are uploaded
   - No server storage needed - saves disk space

2. **Local Storage (Fallback)**:
   - If Google Drive is not configured, pictures save to `webapp/static/uploads/profiles/`
   - Works offline and without any setup
   - Suitable for development and testing

## Setup Google Drive (Optional but Recommended)

Follow the detailed guide in **GOOGLE_DRIVE_SETUP.md** for step-by-step instructions.

### Quick Setup (5 minutes):

1. **Create Google Cloud Project** and enable Drive API
2. **Create Service Account** and download JSON credentials
3. **Create Drive Folder** named "SmartApply Profile Pictures"
4. **Share folder** with service account email (from JSON file)
5. **Add to .env**:
   ```env
   GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
   GOOGLE_DRIVE_CREDENTIALS_FILE=google-drive-credentials.json
   ```
6. **Place credentials** file in project root

## Current Implementation Features

### Upload Process
- Validates file type (PNG, JPG, JPEG, GIF, WEBP)
- Validates file size (max 5MB)
- Client-side preview before upload
- Generates unique filenames with timestamps
- Deletes old pictures automatically

### Display Logic
- Automatically detects Google Drive URLs vs local paths
- Shows profile picture in:
  - Profile page (180x180px circular)
  - Header dropdown (small circular)
  - User menu dropdown

### Fallback Behavior
```
Try Google Drive Upload
  ↓
  Success? → Store Google Drive URL → Done
  ↓
  Failed? → Upload Locally → Store Local Path → Done
```

### Security
- Service account credentials (not user OAuth)
- Files set to "Anyone with link can view"
- Credentials excluded from git (.gitignore)
- Secure filename generation

## Files Modified/Created

### Created:
- `services/google_drive.py` - Google Drive service helper
- `migrations/add_profile_picture.py` - Database migration
- `GOOGLE_DRIVE_SETUP.md` - Detailed setup guide
- `PROFILE_UPLOAD_GUIDE.md` - This file

### Modified:
- `models/user.py` - Added `profile_picture` field
- `routes/dashboard.py` - Added upload logic with Google Drive integration
- `templates/dashboard/user/profile.html` - Profile page with upload UI
- `templates/dashboard/components/header.html` - Display profile picture
- `requirements.txt` - Added Google Drive API packages
- `.env.example` - Added Google Drive configuration
- `.gitignore` - Excluded credentials files

## Usage for Users

1. **Navigate to Profile**: Click "Profile" in sidebar
2. **Click Camera Icon**: On profile picture
3. **Select Image**: Choose PNG/JPG/JPEG/GIF/WEBP (max 5MB)
4. **Preview**: Image shows immediately
5. **Save Changes**: Click "Save Changes" button
6. **Confirmation**: Success message appears

## Testing

### Without Google Drive:
```bash
cd webapp
python app.py
# Navigate to http://localhost:5000/dashboard/user/profile
# Upload a picture - it will save locally
```

### With Google Drive:
```bash
# After completing setup in GOOGLE_DRIVE_SETUP.md
cd webapp
python app.py
# Upload a picture - check Google Drive folder for the file
# Verify picture displays correctly in dashboard
```

## Troubleshooting

### "Google Drive service not initialized"
- Check if credentials file exists
- Verify environment variables in `.env`
- System will fall back to local storage

### Pictures not displaying
- Check browser console for errors
- Verify file permissions (for local storage)
- Verify Google Drive link is publicly accessible

### Upload fails
- Check file size (max 5MB)
- Check file type (must be image)
- Check server logs for specific error

## API Limits

Google Drive Free Tier:
- **Storage**: 15 GB (shared with Gmail & Photos)
- **API Calls**: 1 billion per day
- **File Size**: Up to 5TB per file

For profile pictures (5MB max), limits are more than sufficient.

## Future Enhancements

Potential improvements:
- Image compression before upload
- Thumbnail generation
- Multiple profile picture sizes
- Crop/rotate functionality
- Upload progress indicator
- Batch upload for admins

## Support

For issues or questions:
1. Check `GOOGLE_DRIVE_SETUP.md` for detailed setup
2. Review server logs for error messages
3. Test with local storage first (no setup needed)
4. Verify credentials and permissions
