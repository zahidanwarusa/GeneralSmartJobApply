# Supabase Storage Setup Guide - Profile Pictures

## Overview

Supabase Storage is now configured for storing profile pictures. This is the simplest and most integrated solution since you're already using Supabase for your database!

## Quick Setup (3 Minutes!)

### Step 1: Access Supabase Dashboard

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Sign in to your account
3. Select your **SmartApply** project

### Step 2: Enable Storage

1. In the left sidebar, click **Storage**
2. You'll see the Storage interface

### Step 3: Create Bucket

1. Click the **"New bucket"** button
2. Fill in the details:
   - **Name**: `profile-pictures`
   - **Public**: ✅ Check this box (makes files publicly accessible)
   - **File size limit**: `5` MB
   - **Allowed MIME types**: Leave empty or add:
     ```
     image/png, image/jpeg, image/jpg, image/gif, image/webp
     ```
3. Click **"Create bucket"**

### Step 4: Configure Bucket Policies (Important!)

1. Click on the `profile-pictures` bucket you just created
2. Click the **"Policies"** tab at the top
3. Click **"New Policy"**
4. Choose **"For full customization"**
5. Add these two policies:

#### Policy 1: Allow Public SELECT (View/Download)
```
Policy name: Public Access
Allowed operation: SELECT
Target roles: public

Policy definition:
true
```

#### Policy 2: Allow Authenticated Users to INSERT/UPDATE/DELETE
```
Policy name: Authenticated Users Full Access
Allowed operation: ALL
Target roles: authenticated

Policy definition:
true
```

**OR** use the quick templates:
- Click "New Policy" → "Get started quickly"
- Select "Enable read access for all users"
- Select "Enable insert access for authenticated users"
- Select "Enable update access for users based on user_id"
- Select "Enable delete access for users based on user_id"

### Step 5: Verify Your Credentials

Your `.env` file should already have these (you're using Supabase for database):

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

That's it! No additional configuration needed!

---

## Testing the Setup

Run this simple test:

```bash
cd webapp
python -c "from services.supabase_storage import get_storage_service; s = get_storage_service(); print('✓ Available' if s.is_available() else '✗ Not available')"
```

Expected output:
```
[SUCCESS] Supabase Storage service initialized successfully
✓ Available
```

---

## How It Works

### Upload Flow
```
User uploads image
      ↓
Validate file (type & size)
      ↓
Generate unique filename (user_123_1234567890.png)
      ↓
Upload to Supabase Storage bucket
      ↓
Get public URL
      ↓
Store URL in database
      ↓
Display in dashboard
```

### URL Format
Uploaded images get a URL like:
```
https://yourproject.supabase.co/storage/v1/object/public/profile-pictures/user_1_1704321600.123.png
```

This URL is:
- ✅ Publicly accessible (no auth required)
- ✅ Served via Supabase CDN (fast globally)
- ✅ Cached by browsers
- ✅ Direct image URL (no redirects)

---

## Features

### ✅ What's Included

- **Automatic Upload**: Profile pictures upload to Supabase automatically
- **Public URLs**: Direct, shareable links to images
- **CDN Delivery**: Fast loading worldwide
- **Old File Deletion**: Automatically removes old profile pictures
- **Fallback**: Falls back to local storage if Supabase unavailable
- **Security**: File type and size validation

### 📊 Supabase Free Tier

- **Storage**: 1 GB
- **Bandwidth**: 2 GB/month (then $0.09/GB)
- **File uploads**: Unlimited
- **File size**: Up to 50MB per file (we limit to 5MB)

For profile pictures (5MB max), this is more than enough for hundreds of users!

---

## Bucket Configuration

### Current Settings
```
Name: profile-pictures
Public: Yes
Max file size: 5 MB
Allowed types: PNG, JPG, JPEG, GIF, WEBP
```

### Recommended Policies

**Policy 1: Public Read Access**
- Allows anyone to view/download images
- Required for displaying profile pictures

**Policy 2: Authenticated Write Access**
- Only logged-in users can upload/update/delete
- Prevents anonymous uploads

---

## Troubleshooting

### Error: "Supabase Storage service not initialized"

**Cause**: Missing or invalid Supabase credentials

**Solution**:
1. Check `.env` file has `SUPABASE_URL` and `SUPABASE_ANON_KEY`
2. Verify the values are correct (copy from Supabase dashboard)
3. Restart your Flask application

### Error: "Bucket not found"

**Cause**: The `profile-pictures` bucket doesn't exist

**Solution**:
1. Go to Supabase Dashboard → Storage
2. Create bucket named exactly `profile-pictures`
3. Make it public
4. Restart application

### Error: "Upload failed" or "Permission denied"

**Cause**: Incorrect bucket policies

**Solution**:
1. Go to bucket → Policies tab
2. Ensure public SELECT policy exists
3. Ensure authenticated users have INSERT/UPDATE/DELETE
4. Test with a fresh upload

### Images not displaying

**Cause**: Bucket is not public or policies are wrong

**Solution**:
1. Verify bucket is set to Public
2. Check policies allow SELECT for public
3. Test the URL directly in browser
4. Check browser console for CORS errors

### "File too large" error

**Cause**: File exceeds 5MB limit

**Solution**:
1. Users should upload smaller images
2. You can increase limit in bucket settings (not recommended)
3. Consider adding client-side compression

---

## Security Considerations

### ✅ What's Protected

- File type validation (only images)
- File size validation (max 5MB)
- Unique filenames (prevents overwriting)
- Automatic old file deletion
- Row Level Security (RLS) via Supabase policies

### ⚠️ Important Notes

1. **Public Buckets**: Images are publicly accessible (intended behavior)
2. **File Names**: Use user ID in filename for organization
3. **Content Validation**: Only client-side image preview (consider server-side validation for production)
4. **Rate Limiting**: Consider adding upload rate limits in production

---

## Comparison: Supabase vs Google Drive

| Feature | Supabase Storage | Google Drive API |
|---------|-----------------|------------------|
| Setup Time | 3 minutes | 15-30 minutes |
| Credentials | Already have | Need service account |
| Integration | Native (same as DB) | External service |
| CDN | ✅ Built-in | ❌ Not included |
| Free Tier | 1 GB storage | 15 GB storage |
| Speed | Very fast | Slower (API calls) |
| Complexity | Simple | Complex |
| Dependencies | 1 package | 3 packages |

**Winner**: Supabase Storage (for this use case)

---

## Advanced Features (Optional)

### Image Transformations

Supabase Storage supports image transformations via URL parameters:

```
# Original
https://project.supabase.co/storage/v1/object/public/profile-pictures/image.png

# Resize to 200x200
https://project.supabase.co/storage/v1/object/public/profile-pictures/image.png?width=200&height=200

# Quality optimization
https://project.supabase.co/storage/v1/object/public/profile-pictures/image.png?quality=80
```

### Automatic Bucket Creation

The code includes `create_bucket()` method that can automatically create the bucket if it doesn't exist. To enable:

```python
# In webapp/services/supabase_storage.py
# Uncomment in __init__ method:
self.create_bucket()
```

---

## Migration from Local Storage

If you have existing profile pictures in local storage:

1. Upload them manually to Supabase bucket
2. Update database:
   ```sql
   UPDATE users
   SET profile_picture = 'https://yourproject.supabase.co/storage/v1/object/public/profile-pictures/user_X_timestamp.png'
   WHERE id = X;
   ```
3. Delete local files (optional)

---

## Monitoring

### Check Usage

1. Go to Supabase Dashboard
2. Click "Settings" → "Billing"
3. View storage usage under "Project Usage"

### View Uploaded Files

1. Go to Supabase Dashboard
2. Click "Storage"
3. Click `profile-pictures` bucket
4. See all uploaded files with size and date

---

## Next Steps

1. ✅ **Test Upload**: Upload a profile picture
2. ✅ **Verify Display**: Check it appears in header and profile page
3. ✅ **Test Update**: Upload a new picture (old one should be deleted)
4. ✅ **Check Bucket**: Verify files in Supabase dashboard

---

## Support

### Common Questions

**Q: Do I need to pay for Supabase?**
A: No, free tier includes 1GB storage which is plenty for profile pictures.

**Q: What happens if I exceed free tier?**
A: Supabase will notify you. You can upgrade or delete old files.

**Q: Can I use this for other files?**
A: Yes! Create different buckets for resumes, documents, etc.

**Q: Is it secure?**
A: Yes, with proper RLS policies. Images are public but only authenticated users can upload.

**Q: What if Supabase is down?**
A: The app automatically falls back to local storage.

### Getting Help

1. Check this guide
2. Run test script: `python test_supabase_storage.py` (create if needed)
3. Check Supabase Dashboard → Logs
4. Check Flask application logs

---

## Summary

✅ **Setup Complete!**

Your profile picture system now uses:
- Supabase Storage for cloud hosting
- Local storage as fallback
- Automatic old file deletion
- Public CDN URLs for fast delivery
- Simple, integrated solution

**Total setup time**: ~3 minutes
**Zero additional credentials needed**
**Works immediately with your existing Supabase project**

Enjoy your new profile picture feature! 🎉
