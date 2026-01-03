# Google Drive API Setup Guide

This guide will help you set up Google Drive API for storing profile pictures.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a project" → "New Project"
3. Enter project name: `SmartApply` (or your preferred name)
4. Click "Create"

## Step 2: Enable Google Drive API

1. In the Google Cloud Console, select your project
2. Go to "APIs & Services" → "Library"
3. Search for "Google Drive API"
4. Click on it and press "Enable"

## Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Enter service account details:
   - Name: `smartapply-drive-service`
   - ID: (auto-generated)
   - Description: "Service account for SmartApply profile picture uploads"
4. Click "Create and Continue"
5. Skip "Grant this service account access to project" (optional)
6. Click "Done"

## Step 4: Create and Download Service Account Key

1. In "Credentials" page, click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. A JSON file will be downloaded - **KEEP THIS SAFE!**

## Step 5: Create Google Drive Folder

1. Go to [Google Drive](https://drive.google.com/)
2. Create a new folder: "SmartApply Profile Pictures"
3. Right-click the folder → "Share"
4. Add the service account email (found in the JSON file as `client_email`)
5. Give it "Editor" permissions
6. Copy the folder ID from the URL:
   - URL format: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Copy the `FOLDER_ID_HERE` part

## Step 6: Configure Environment Variables

Add the following to your `.env` file:

```env
# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_DRIVE_CREDENTIALS_FILE=path/to/your/credentials.json
```

**OR** you can store credentials as JSON string:

```env
# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_DRIVE_CREDENTIALS={"type":"service_account","project_id":"...","private_key_id":"..."}
```

## Step 7: Place Credentials File

Option A: **Store credentials as file (Recommended for development)**
1. Place the downloaded JSON file in your project root
2. Rename it to `google-drive-credentials.json`
3. Update `.env`: `GOOGLE_DRIVE_CREDENTIALS_FILE=google-drive-credentials.json`
4. Add to `.gitignore`: `google-drive-credentials.json`

Option B: **Store credentials as environment variable (Recommended for production)**
1. Copy the entire content of the JSON file
2. Minify it (remove spaces and newlines)
3. Add to `.env`: `GOOGLE_DRIVE_CREDENTIALS={"type":"service_account",...}`

## Step 8: Test the Setup

Run your Flask application and try uploading a profile picture. Check:
1. The file appears in your Google Drive folder
2. The profile picture displays correctly in the dashboard
3. Check server logs for any errors

## Important Security Notes

1. **Never commit credentials to Git!** Add to `.gitignore`:
   ```
   google-drive-credentials.json
   *.json
   .env
   ```

2. **Rotate credentials periodically** for security

3. **Use environment variables in production** (Option B above)

4. **Limit service account permissions** - only give access to the specific folder

## Troubleshooting

### Error: "Google Drive service not initialized"
- Check if credentials file exists at the specified path
- Verify the JSON file is valid
- Ensure environment variables are set correctly

### Error: "File not found" or "Permission denied"
- Verify the folder ID is correct
- Make sure the service account has Editor access to the folder
- Check if the folder still exists in Google Drive

### Profile pictures not displaying
- Verify the file was uploaded successfully (check Google Drive folder)
- Check if the file permissions are set to "Anyone with the link can view"
- Ensure the direct link format is correct

## Fallback Mode

If Google Drive is not configured, the application will automatically fall back to local storage:
- Files will be stored in `webapp/static/uploads/profiles/`
- No additional configuration needed
- Works offline

## API Limits

Google Drive API has the following limits:
- **Queries per day**: 1,000,000,000
- **Queries per 100 seconds per user**: 1,000
- **Upload size limit**: 5TB per file

For SmartApply profile pictures (max 5MB), these limits are more than sufficient.
