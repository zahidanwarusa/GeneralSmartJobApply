# Two-Factor Authentication (2FA) Implementation Plan

## Summary
I've started implementing 2FA but it's a substantial feature. Given the complexity and current token usage, I recommend we:

1. **Save current progress** (fields added to User model)
2. **Run database migration** to add the 2FA fields
3. **Continue in next session** with routes and UI

## What's Been Completed:

### ✅ Libraries Installed:
- `pyotp` - For generating and verifying TOTP codes
- `qrcode[pil]` - For generating QR codes

### ✅ User Model Updated:
Added fields:
- `two_factor_enabled` (Boolean) - Whether 2FA is active
- `two_factor_secret` (String) - TOTP secret key
- `backup_codes` (Text/JSON) - Emergency backup codes

Added methods:
- `generate_2fa_secret()` - Creates TOTP secret
- `get_2fa_uri()` - Gets provisioning URI for QR code
- `verify_2fa_token(token)` - Verifies 6-digit code
- `generate_backup_codes(count)` - Creates backup codes
- `verify_backup_code(code)` - Uses backup code
- `enable_2fa()` - Turns on 2FA
- `disable_2fa()` - Turns off 2FA

## What's Remaining:

### 1. Database Migration
Run migration to add 2FA fields to database

### 2. Routes (10+ routes needed):
- `GET/POST /auth/two-factor-setup` - QR code setup page
- `POST /auth/two-factor-verify-setup` - Verify initial setup
- `GET /auth/two-step-verification` - Login 2FA check
- `POST /auth/verify-2fa` - Verify code during login
- `GET/POST /auth/settings/two-factor` - Enable/disable page
- `POST /auth/settings/disable-two-factor` - Turn off 2FA
- `GET /auth/backup-codes` - View backup codes
- `POST /auth/regenerate-backup-codes` - New backup codes

### 3. Update Login Flow:
- Check if user has 2FA enabled after password verification
- Redirect to 2FA verification instead of logging in
- Store temporary session data
- Verify 2FA code before completing login

### 4. Templates (5+ pages):
- `two-factor-setup.html` - QR code & setup instructions
- `two-step-verification.html` - Login 2FA entry page
- `two-factor-settings.html` - Enable/disable 2FA
- `backup-codes.html` - Display backup codes
- `two-factor-disable-confirm.html` - Confirmation page

### 5. QR Code Generation:
- Generate QR code image from TOTP URI
- Display on setup page
- Manual entry code option

### 6. Session Management:
- Temporary storage of user ID during 2FA verification
- Prevent bypassing 2FA check
- Secure token generation

## Recommended Next Steps:

### Option A: Quick Migration & Basic Implementation (30 min)
1. Run database migration
2. Add basic 2FA setup route
3. Add basic 2FA verification route
4. Create minimal templates
5. Test with Google Authenticator

### Option B: Full Professional Implementation (2-3 hours)
1. All routes with full validation
2. Professional UI/UX
3. Backup codes management
4. Account recovery flow
5. Settings integration
6. Comprehensive testing
7. Documentation

### Option C: Continue Later
1. Save current progress ✓
2. Run migration when ready
3. Continue implementation in next session

## Quick Migration Script

I can create a migration script right now to add the 2FA fields to your database. Would you like me to:

**A)** Create & run the migration now (5 minutes)
**B)** Complete basic 2FA implementation (30 minutes)
**C)** Full implementation (continue in next session)

Let me know how you'd like to proceed!
