# Email Verification System Implementation

## Overview
This document describes the email verification system implemented for SmartApply Pro. Users must verify their email address with a 6-digit code sent to them after registration or when logging in with an unverified email.

## Database Changes

### New Fields Added to `users` Table:
- `email_verified` (BOOLEAN, default: FALSE) - Tracks if email is verified
- `verification_code` (VARCHAR(6)) - Stores the 6-digit verification code
- `verification_code_expires` (TIMESTAMP) - Expiration time for the code (15 minutes)

### Migration Script:
Run the migration to add these fields:
```bash
cd webapp
python run_email_verification_migration.py
```

## Features Implemented

### 1. **Registration Flow**
- User completes registration form (2 steps)
- System generates a 6-digit verification code
- Code is stored in database with 15-minute expiration
- User is redirected to `/auth/email-verification`
- Code is printed to console (TODO: send via email)

### 2. **Login Flow**
- User attempts to log in
- System checks if `email_verified` is FALSE
- If unverified:
  - Generates new 6-digit code
  - Redirects to `/auth/email-verification`
  - Code is printed to console (TODO: send via email)
- If verified:
  - Proceeds with normal login

### 3. **Verification Page** (`/auth/email-verification`)
- Displays 6 input boxes for code digits
- Auto-focuses next input as user types
- Auto-submits when all 6 digits are entered
- Shows countdown timer for resend (60 seconds)
- Validates code on submit:
  - Success: Marks `email_verified = TRUE`, logs in user
  - Failure: Shows error message

### 4. **Resend Code** (`/resend-verification-code`)
- AJAX endpoint to resend verification code
- Generates new 6-digit code
- Updates expiration time
- Returns JSON response
- 60-second cooldown timer

## User Model Methods

### `generate_verification_code()`
```python
def generate_verification_code(self):
    """Generate a 6-digit verification code"""
    import random
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    self.verification_code = code
    self.verification_code_expires = datetime.utcnow() + timedelta(minutes=15)
    return code
```

### `verify_code(code)`
```python
def verify_code(self, code):
    """Verify if the provided code matches and is not expired"""
    if not self.verification_code or not self.verification_code_expires:
        return False
    if datetime.utcnow() > self.verification_code_expires:
        return False
    return self.verification_code == code
```

## Routes Added

### `GET/POST /auth/email-verification`
- Displays verification form
- Processes verification code submission
- Verifies code and logs in user on success

### `POST /auth/resend-verification-code`
- JSON endpoint to resend verification code
- Returns success/failure response

## Frontend Features

### Email Verification Page:
1. **6-Digit Code Input**
   - Individual input boxes for each digit
   - Auto-advance to next input
   - Paste support (Ctrl+V)
   - Numeric-only validation

2. **Auto-Submit**
   - Automatically submits form when all 6 digits are entered
   - 300ms delay for user confirmation

3. **Resend Functionality**
   - "Resend Code" button
   - 60-second countdown timer
   - Disables during countdown
   - AJAX request to backend

4. **Responsive Design**
   - Clean, centered layout
   - Bootstrap styling
   - Mobile-friendly

## Security Features

1. **Code Expiration**: Verification codes expire after 15 minutes
2. **One-Time Use**: Code is cleared after successful verification
3. **Session-Based**: Email stored in session for verification process
4. **Rate Limiting**: 60-second cooldown between resend requests

## TODO: Email Integration

Currently, verification codes are printed to the console. To integrate email sending:

1. **Install Email Library**:
   ```bash
   pip install Flask-Mail
   ```

2. **Configure Email Settings** in `.env`:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@smartapplypro.com
   ```

3. **Replace Console Logging** with Email Sending:
   ```python
   # In auth.py, replace:
   print(f"[VERIFICATION CODE] Email: {user.email}, Code: {code}")

   # With:
   send_verification_email(user.email, code)
   ```

4. **Create Email Template**:
   - Subject: "Verify Your SmartApply Pro Account"
   - Body: Include the 6-digit code and expiration time
   - Add company branding

## Testing the System

1. **Register a New User**:
   - Fill out registration form
   - Submit form
   - Should redirect to `/auth/email-verification`
   - Check console for verification code

2. **Enter Verification Code**:
   - Type the 6-digit code from console
   - Should auto-submit after 6th digit
   - Should log in and redirect to dashboard

3. **Test Code Expiration**:
   - Wait 15 minutes after generating code
   - Try to verify with expired code
   - Should show "Invalid or expired verification code"

4. **Test Resend**:
   - Click "Resend Code" button
   - Check console for new code
   - Verify with new code

5. **Test Login with Unverified Email**:
   - Create user but don't verify
   - Log out
   - Try to log in
   - Should redirect to verification page

## Files Modified/Created

### Modified:
- `webapp/models/user.py` - Added verification fields and methods
- `webapp/routes/auth.py` - Added verification routes and checks
- `webapp/routes/auth.py` (imports) - Added `jsonify` and `datetime`

### Created:
- `webapp/run_email_verification_migration.py` - Database migration script
- `webapp/templates/auth/email_verification.html` - Verification page template
- `EMAIL_VERIFICATION_SETUP.md` - This documentation file

## Flow Diagrams

### Registration Flow:
```
User fills form → Submit → Create user → Generate code →
Print to console → Redirect to /auth/email-verification →
User enters code → Verify → Login → Dashboard
```

### Login Flow (Unverified Email):
```
User enters credentials → Check password → Check email_verified →
If FALSE: Generate code → Print to console →
Redirect to /auth/email-verification → User enters code →
Verify → Login → Dashboard
```

### Login Flow (Verified Email):
```
User enters credentials → Check password → Check email_verified →
If TRUE: Login → Dashboard
```

## Support

For issues or questions about email verification:
1. Check console logs for verification codes (development)
2. Verify database migration ran successfully
3. Check that `email_verified` field exists in users table
4. Ensure session is properly configured in Flask app
