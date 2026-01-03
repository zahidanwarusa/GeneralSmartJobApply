# Supabase Bucket Policies Setup - Visual Guide

## ✅ Step 1: Bucket Created!

The `profile-pictures` bucket has been created successfully by the setup script.

## 📋 Step 2: Configure Policies (2 minutes)

The bucket needs policies to control who can read/write files. Follow these steps:

### A. Access Your Supabase Dashboard

1. Go to: **https://supabase.com/dashboard**
2. Sign in if needed
3. Select your **SmartApply project**

### B. Navigate to Storage Policies

1. Click **"Storage"** in the left sidebar
2. You'll see your `profile-pictures` bucket
3. Click on the **`profile-pictures`** bucket
4. Click the **"Policies"** tab at the top

### C. Add Policy 1: Public Read Access

This allows anyone to view profile pictures.

1. Click **"New Policy"** button
2. Click **"Get started quickly"**
3. Select: **"Enable read access for all users"**
4. Leave everything as default
5. Click **"Review"**
6. Click **"Save policy"**

✅ Now anyone can view profile pictures!

### D. Add Policy 2: Authenticated Insert

This allows logged-in users to upload pictures.

1. Click **"New Policy"** button again
2. Click **"Get started quickly"**
3. Select: **"Enable insert for authenticated users only"**
4. Leave everything as default
5. Click **"Review"**
6. Click **"Save policy"**

✅ Now authenticated users can upload!

### E. Add Policy 3: Authenticated Update

This allows users to update their pictures.

1. Click **"New Policy"** button again
2. Click **"Get started quickly"**
3. Select: **"Enable update for users based on user_id"**
4. Leave everything as default
5. Click **"Review"**
6. Click **"Save policy"**

✅ Now users can update their pictures!

### F. Add Policy 4: Authenticated Delete

This allows cleanup of old pictures.

1. Click **"New Policy"** button again
2. Click **"Get started quickly"**
3. Select: **"Enable delete for users based on user_id"**
4. Leave everything as default
5. Click **"Review"**
6. Click **"Save policy"**

✅ Now old pictures can be deleted!

---

## Alternative: Manual Policy Creation

If the templates don't work, create custom policies:

### Policy 1: Public SELECT (Read)
```
Policy name: Public Read Access
Allowed operation: SELECT
Target roles: public
Policy definition: true
```

### Policy 2: Authenticated INSERT (Upload)
```
Policy name: Authenticated Insert
Allowed operation: INSERT
Target roles: authenticated
Policy definition: true
```

### Policy 3: Authenticated UPDATE (Modify)
```
Policy name: Authenticated Update
Allowed operation: UPDATE
Target roles: authenticated
Policy definition: true
```

### Policy 4: Authenticated DELETE (Remove)
```
Policy name: Authenticated Delete
Allowed operation: DELETE
Target roles: authenticated
Policy definition: true
```

---

## ✅ Step 3: Test It!

1. **Go to your app**: http://localhost:5000/dashboard/user/profile
2. **Click camera icon** on profile picture
3. **Select an image** (PNG, JPG, JPEG, GIF, WEBP, max 5MB)
4. **Click "Save Changes"**
5. **Success!** You should see: "Profile picture uploaded successfully!"

---

## Verify Upload in Supabase Dashboard

1. Go to **Storage** → **profile-pictures** bucket
2. You should see your uploaded file: `user_{id}_{timestamp}.{ext}`
3. Click on the file to preview it
4. Copy the public URL and test it in a browser

---

## Troubleshooting

### Still getting "uploaded locally"?

**Check 1**: Verify bucket exists
- Go to Storage in Supabase Dashboard
- Confirm `profile-pictures` bucket is there

**Check 2**: Verify policies are configured
- Click bucket → Policies tab
- Should see 4 policies (SELECT, INSERT, UPDATE, DELETE)

**Check 3**: Test the service
```bash
cd webapp
python -c "from services.supabase_storage import get_storage_service; s = get_storage_service(); print('Available:', s.is_available()); print('Bucket exists:', s.check_bucket_exists())"
```

Should show:
```
Available: True
Bucket exists: True
```

**Check 4**: Try uploading again
- Restart your Flask app
- Upload a new profile picture
- Check for success message

### "Permission denied" error?

- Make sure policies are configured correctly
- Verify you're logged in (authenticated user)
- Check Supabase Dashboard → Logs for details

### Upload works but picture doesn't display?

- Verify bucket is set to **Public**
- Check Policy 1 (SELECT for public) exists
- Test the URL directly in browser
- Clear browser cache

---

## Summary

After completing these steps:

✅ Bucket created: `profile-pictures`
✅ Bucket is public
✅ Policies configured (4 policies)
✅ Ready to upload profile pictures!

Now try uploading a profile picture and it should work! 🎉
