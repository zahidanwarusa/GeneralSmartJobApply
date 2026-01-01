# Database & User Management Guide

## Understanding Your Database Setup

Your app uses **TWO different databases**:

### 1. Supabase Auth (auth.users)
- **Location**: Supabase Dashboard → Authentication → Users
- **Purpose**: OAuth authentication (Google login, etc.)
- **Managed by**: Supabase Auth API

### 2. PostgreSQL Database (public.users)
- **Location**: Supabase PostgreSQL → Table Editor → users table
- **Purpose**: Your app's user data (profiles, verification codes, etc.)
- **Managed by**: Your Flask app

## The Problem

When you:
1. Delete user from Supabase **Authentication** tab
2. Sign up again
3. User gets created in **auth.users** (Supabase Auth)
4. But old user still exists in **public.users** (your app's table)
5. Verification fails because of duplicate/mismatch

---

## Solution: Properly Delete Users

### Method 1: Delete from PostgreSQL (Recommended)

**Use the reset script:**

```bash
cd webapp
python reset_user_account.py
```

This will:
- Show all users in your database
- Let you delete specific users
- Clean up the `public.users` table

### Method 2: Delete from Supabase Dashboard

**Step 1 - Delete from PostgreSQL:**
1. Go to: https://supabase.com/dashboard
2. Select your project
3. Click **Table Editor** (left sidebar)
4. Click **users** table
5. Find the user row
6. Click the 3 dots → Delete
7. Confirm deletion

**Step 2 - Delete from Auth (optional):**
1. Click **Authentication** (left sidebar)
2. Click **Users** tab
3. Find the user
4. Click 3 dots → Delete User
5. Confirm deletion

---

## Quick Fix for Your Current Situation

You have a user `zahidsdet@gmail.com` with code **863949**.

### Option A: Use Current Code

Just received a fresh email with code **863949**:

1. Check your Gmail inbox
2. Find the verification email
3. Use code: **863949**
4. Verify your account

### Option B: Start Fresh

Delete current user and register again:

```bash
cd webapp
python delete_user.py
```

Then register at: http://localhost:5000/auth/register

---

## Checking Your Database Status

### See all users:
```bash
cd webapp
python check_user.py
```

### Send new verification code:
```bash
cd webapp
python send_new_code.py
```

### Manually verify a user:
```bash
cd webapp
python verify_user.py
```

---

## Common Scenarios

### Scenario 1: "I deleted from Supabase Auth but user still exists"

**Problem**: You deleted from Authentication tab, not PostgreSQL table

**Fix**:
```bash
cd webapp
python reset_user_account.py
```

### Scenario 2: "Verification code doesn't work"

**Problem**: Code might be expired or wrong

**Fix**:
```bash
cd webapp
python check_user.py  # See current code
python send_new_code.py  # Get fresh code via email
```

### Scenario 3: "I want to start completely fresh"

**Fix**:
```bash
cd webapp
python reset_user_account.py
# Enter 'all' to delete all users
```

Then register again from the web interface.

---

## Understanding the Flow

### Registration Flow:
```
User registers
    ↓
User created in public.users (PostgreSQL)
    ↓
Verification code generated
    ↓
Email sent with code
    ↓
User enters code
    ↓
email_verified = True
    ↓
User can log in
```

### OAuth Flow (Google):
```
User clicks "Login with Google"
    ↓
Redirected to Google
    ↓
Google auth successful
    ↓
User created in auth.users (Supabase Auth)
    ↓
Check if user exists in public.users
    ↓
If not, redirect to complete signup form
    ↓
User fills additional info
    ↓
User created in public.users
    ↓
Logged in
```

---

## Your Current Status

**Database**: Supabase PostgreSQL
**User**: zahidsdet@gmail.com
**Code**: 863949
**Expires**: 15 minutes from now
**Email**: Just sent ✓

**Action**: Check your Gmail and use code 863949

---

## Prevention Tips

1. **Don't delete users from Supabase Dashboard**
   - Use the reset script instead
   - Or delete from both auth.users AND public.users

2. **Always check database before testing**
   ```bash
   python check_user.py
   ```

3. **Use email resend if code expires**
   ```bash
   python send_new_code.py
   ```

4. **For testing, use the same email (zahidsdet@gmail.com)**
   - Resend works perfectly
   - No need to delete and recreate

---

## Need to Test Full Registration Flow?

If you want to test the complete flow from scratch:

1. **Delete current user**:
   ```bash
   cd webapp
   python reset_user_account.py
   ```

2. **Start Flask app**:
   ```bash
   cd webapp
   python app.py
   ```

3. **Register at**: http://localhost:5000/auth/register
   - Use: zahidsdet@gmail.com
   - Choose username and password
   - Fill all required fields

4. **Check Gmail** for verification email

5. **Enter code** on verification page

6. **You're in!**

---

## Summary

✅ **Current situation**: You have a valid user with code 863949
✅ **Email sent**: Check your Gmail inbox
✅ **Quick fix**: Just use the code from email
✅ **Long-term**: Use the management scripts

**Next step**: Check your Gmail for code 863949 and verify your account!
