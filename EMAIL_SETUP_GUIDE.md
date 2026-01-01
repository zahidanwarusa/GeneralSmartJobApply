# Email Setup Guide for SmartApply Pro

## Overview
Your application now has a complete email verification system that sends beautiful HTML emails with 6-digit verification codes. The system uses **Resend** for email delivery with automatic console fallback for development.

## Current Status
✅ Email service implemented and integrated
✅ Resend library installed
✅ Console fallback working (codes print to terminal)
⚠️ **Action Required**: Configure Resend API key to send actual emails

---

## Option 1: Use Resend (Recommended - FREE)

### Why Resend?
- **Free Tier**: 3,000 emails/month, 100 emails/day
- **Simple Setup**: Takes 5 minutes
- **Great Deliverability**: Built by the creators of React Email
- **No Credit Card Required** for free tier

### Setup Steps:

#### 1. Create Resend Account
1. Go to https://resend.com
2. Click "Start Building" or "Sign Up"
3. Sign up with your email or GitHub account
4. Verify your email address

#### 2. Get Your API Key
1. Once logged in, you'll see the dashboard
2. Click on "API Keys" in the left sidebar
3. Your API key will be visible (starts with `re_`)
4. Click "Copy" to copy your API key

#### 3. Add API Key to .env File
1. Open `webapp/.env` file
2. Find the line: `RESEND_API_KEY=`
3. Paste your API key after the `=`
   ```
   RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. Save the file

#### 4. Configure Domain (Optional but Recommended)

**For Testing (Use Default):**
- The default email `onboarding@resend.dev` works immediately
- You can send emails right away for testing
- **Limitation**: Can only send to YOUR verified email address

**For Production (Add Your Domain):**
1. In Resend dashboard, click "Domains" → "Add Domain"
2. Enter your domain (e.g., `smartapplypro.com`)
3. Add the DNS records shown by Resend to your domain provider
4. Wait for verification (usually 5-15 minutes)
5. Update `.env` file:
   ```
   FROM_EMAIL=noreply@yourdomain.com
   ```

---

## Option 2: Use Gmail SMTP (Alternative)

If you prefer to use Gmail instead:

### Setup Steps:

#### 1. Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" if not already enabled

#### 2. Create App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select your device
4. Click "Generate"
5. Copy the 16-character password

#### 3. Update .env File
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

#### 4. Update Email Service
You'll need to modify `services/email_service.py` to use Flask-Mail instead of Resend. (Let me know if you want to go this route)

---

## Testing Email Functionality

### With Console Fallback (Current Setup)
1. Start your Flask app:
   ```bash
   cd webapp
   python app.py
   ```
2. Register a new user
3. Check the terminal/console for the verification code
4. Enter the code on the verification page

### With Resend Configured
1. Add your Resend API key to `.env`
2. Restart your Flask app
3. Register with YOUR email address (the one you used for Resend)
4. Check your inbox for the verification email
5. Enter the 6-digit code

**Important**: With Resend's default domain, you can only send to:
- The email you used to sign up for Resend
- Other emails you verify in Resend dashboard

---

## Email Templates

Your verification emails include:
- **Professional HTML design** with your branding
- **6-digit verification code** prominently displayed
- **15-minute expiration notice**
- **Security warnings** about not sharing the code
- **Responsive design** that works on all devices
- **Plain text fallback** for email clients that don't support HTML

---

## Troubleshooting

### "No verification code received"
1. **Check spam/junk folder**
2. **Verify Resend API key** is correct in `.env`
3. **Check console output** - the code is always printed to terminal as backup
4. **Restart Flask app** after changing `.env`

### "Failed to send email" in console
1. **Check API key** is set correctly
2. **Verify email domain** (use default `onboarding@resend.dev` for testing)
3. **Check Resend dashboard** for delivery status
4. The system will still work - code is shown in console

### "Can't send to other emails"
- With `onboarding@resend.dev`, you can only send to your Resend account email
- **Solution**: Add and verify your own domain in Resend

---

## Production Deployment

### Before Going Live:

1. ✅ **Add Your Domain to Resend**
   - Verify DNS records
   - Update `FROM_EMAIL` in `.env`

2. ✅ **Set Environment Variables**
   ```bash
   RESEND_API_KEY=your_production_key
   FROM_EMAIL=noreply@yourdomain.com
   SUPPORT_EMAIL=support@yourdomain.com
   ```

3. ✅ **Test Email Deliverability**
   - Send test emails to Gmail, Outlook, Yahoo
   - Check spam scores
   - Verify all links work

4. ✅ **Monitor Email Sending**
   - Check Resend dashboard for delivery rates
   - Set up alerts for failed emails
   - Monitor bounce rates

---

## Cost Breakdown

### Resend Free Tier
- **3,000 emails/month** (free forever)
- **100 emails/day** limit
- Perfect for small to medium applications

### Resend Paid Plans (if you exceed free tier)
- **$20/month**: 50,000 emails
- **$80/month**: 100,000 emails
- Very affordable compared to competitors

### Gmail SMTP
- **Free** but limited to 500 emails/day
- Not recommended for production
- Higher chance of landing in spam

---

## Quick Start (TL;DR)

**To get emails working RIGHT NOW:**

1. Go to https://resend.com and sign up
2. Copy your API key from the dashboard
3. Open `webapp/.env` and add:
   ```
   RESEND_API_KEY=re_your_key_here
   ```
4. Restart your Flask app
5. Register with the email you used for Resend
6. Check your inbox!

---

## Support

Need help? Check:
1. Resend documentation: https://resend.com/docs
2. Resend Discord: https://resend.com/discord
3. Console output for error messages

---

## Files Modified

- ✅ `webapp/services/email_service.py` - Created email service with Resend
- ✅ `webapp/routes/auth.py` - Integrated email sending
- ✅ `webapp/.env` - Added email configuration
- ✅ Installed `resend` package
- ✅ Installed `Flask-Mail` package (optional fallback)
