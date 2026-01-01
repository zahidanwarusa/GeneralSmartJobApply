# Supabase Email Setup Guide

## Overview
This guide will help you configure Supabase to send verification emails for your SmartApply Pro application.

## Two Options for Email Delivery

### Option A: Use Supabase's Built-in SMTP (Recommended)
Supabase can send emails using its own infrastructure or your custom SMTP provider.

### Option B: Use External Provider (Resend/SendGrid)
Configure an external email service that integrates with your app directly.

---

## Option A: Supabase SMTP Configuration

### Step 1: Access Supabase Dashboard
1. Go to https://supabase.com
2. Login to your account
3. Select your project: **aybnkljfursiwkximpvf**

### Step 2: Navigate to Email Settings
1. Click on **Authentication** in the left sidebar
2. Click on **Email Templates** tab
3. You'll see options for:
   - Templates (Confirm signup, Magic Link, etc.)
   - SMTP Settings

### Step 3: Configure Custom SMTP (Optional but Recommended)

#### Why Custom SMTP?
- Better deliverability
- Your own domain name
- Higher email limits
- Professional appearance

#### Recommended SMTP Providers:

**1. Resend (Easiest & Free)**
- Free: 3,000 emails/month
- Sign up: https://resend.com
- SMTP credentials available in dashboard

**Configuration:**
```
SMTP Host: smtp.resend.com
SMTP Port: 587
SMTP User: resend
SMTP Password: [Your Resend API Key]
Sender Email: noreply@yourdomain.com (or onboarding@resend.dev for testing)
```

**2. Gmail SMTP (Free but Limited)**
- Free: 500 emails/day
- Use App Password (not regular password)

**Configuration:**
```
SMTP Host: smtp.gmail.com
SMTP Port: 587
SMTP User: your-email@gmail.com
SMTP Password: [16-character App Password]
Sender Email: your-email@gmail.com
```

**3. SendGrid (Scalable)**
- Free: 100 emails/day
- Sign up: https://sendgrid.com

**Configuration:**
```
SMTP Host: smtp.sendgrid.net
SMTP Port: 587
SMTP User: apikey
SMTP Password: [Your SendGrid API Key]
Sender Email: noreply@yourdomain.com
```

### Step 4: Enable Custom SMTP in Supabase

1. In **Authentication** → **Email Templates** → **SMTP Settings**
2. Toggle **Enable Custom SMTP** to ON
3. Enter your SMTP credentials:
   - **Sender email**: Your from email address
   - **Sender name**: SmartApply Pro
   - **Host**: Your SMTP host (see above)
   - **Port**: Usually 587
   - **Username**: Your SMTP username
   - **Password**: Your SMTP password/API key
4. Click **Save**

### Step 5: Customize Email Template (Optional)

Supabase has built-in templates, but we're using our custom HTML templates. However, you can still customize:

1. Go to **Authentication** → **Email Templates**
2. Click on **Confirm signup** template
3. You can customize the default Supabase email template if needed

---

## Option B: Direct Integration (Current Setup)

Our app currently uses direct email integration with these providers:

### Priority Order:
1. **Supabase** (if SMTP configured)
2. **Resend** (if API key provided)
3. **Console Fallback** (for development)

### Current Environment Variables:

```env
# Supabase Configuration (Already Set)
SUPABASE_URL=https://aybnkljfursiwkximpvf.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Email Service (Configure One)
RESEND_API_KEY=          # Get from https://resend.com
FROM_EMAIL=noreply@smartapplypro.com
SUPPORT_EMAIL=support@smartapplypro.com
```

---

## Quick Setup Steps

### Fastest Way to Get Emails Working:

#### Method 1: Use Resend with Supabase SMTP

1. **Sign up for Resend**
   - Go to https://resend.com
   - Create free account
   - Get your API key from dashboard

2. **Configure Supabase SMTP**
   - Login to Supabase dashboard
   - Go to Authentication → Email Templates → SMTP Settings
   - Enable Custom SMTP
   - Enter Resend credentials:
     ```
     Host: smtp.resend.com
     Port: 587
     User: resend
     Password: [Your Resend API Key]
     Sender: onboarding@resend.dev (for testing)
     ```
   - Click Save

3. **Test It**
   - Register a new user in your app
   - Check your email inbox
   - You should receive a professional verification email

#### Method 2: Use Gmail SMTP (Quick Test)

1. **Create Gmail App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Generate password for "Mail"
   - Copy the 16-character password

2. **Configure Supabase SMTP**
   - Go to Supabase dashboard
   - Authentication → Email Templates → SMTP Settings
   - Enable Custom SMTP:
     ```
     Host: smtp.gmail.com
     Port: 587
     User: your-email@gmail.com
     Password: [16-char app password]
     Sender: your-email@gmail.com
     ```

3. **Test It**
   - Register with any email
   - Check inbox for verification code

---

## Testing Email Delivery

### Check Console Output

When you run your app, you'll see:
```
[EMAIL SERVICE] Supabase client initialized successfully
[EMAIL SERVICE] Email sent successfully via Supabase to user@example.com
```

Or if using fallback:
```
[EMAIL SERVICE] Using console fallback for emails
============================================================
[EMAIL SERVICE] CONSOLE FALLBACK - Email details:
To: user@example.com
Subject: Verify Your SmartApply Pro Account
Verification Code: 123456
============================================================
```

### Verify Email Delivery

1. Register a new user
2. Check your email inbox (and spam folder!)
3. You should see an email from your configured sender
4. Email includes:
   - Professional HTML design
   - 6-digit verification code
   - 15-minute expiration notice
   - Security warnings

---

## Troubleshooting

### "Email not received"

**Check:**
1. ✅ Spam/Junk folder
2. ✅ SMTP settings are correct in Supabase
3. ✅ Sender email is verified (for custom domains)
4. ✅ Console shows success message
5. ✅ Email service provider has credits/quota

### "SMTP connection failed"

**Solutions:**
- Verify SMTP credentials are correct
- Check port number (587 for TLS, 465 for SSL)
- Ensure firewall allows SMTP connections
- Try different SMTP provider

### "Invalid sender email"

**For Resend:**
- Use `onboarding@resend.dev` for testing
- Add and verify your domain for production

**For Gmail:**
- Must use the same email as SMTP user
- Must use App Password, not regular password

### "Rate limit exceeded"

**Provider Limits:**
- Gmail: 500/day
- Resend Free: 100/day, 3,000/month
- SendGrid Free: 100/day

**Solution:** Upgrade plan or use different provider

---

## Production Checklist

Before going live:

- [ ] Custom SMTP configured in Supabase
- [ ] Own domain verified with email provider
- [ ] FROM_EMAIL uses your domain
- [ ] Test emails to multiple providers (Gmail, Outlook, Yahoo)
- [ ] Check spam scores
- [ ] Monitor delivery rates in provider dashboard
- [ ] Set up email rate limiting
- [ ] Configure bounce handling
- [ ] Add unsubscribe link (for marketing emails)

---

## Monitoring Email Delivery

### Supabase Dashboard
- No direct email monitoring
- Check Authentication logs for user activity

### Resend Dashboard
- View all sent emails
- Check delivery status
- See open rates (if tracking enabled)
- Monitor bounce rates

### Gmail Search Console
- Check email deliverability
- View spam reports
- Monitor authentication (SPF, DKIM)

---

## Cost Comparison

| Provider | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Resend** | 3,000/mo | $20/mo (50k) | Production apps |
| **Gmail** | 500/day | N/A | Testing only |
| **SendGrid** | 100/day | $20/mo (50k) | High volume |
| **Mailgun** | 5,000/mo | $35/mo (50k) | Developers |

---

## Current Status

✅ **Implemented:**
- Email service with Supabase integration
- Resend fallback support
- Console logging for development
- HTML email templates
- Verification code system

⚠️ **Action Required:**
- Configure SMTP in Supabase dashboard
- OR add RESEND_API_KEY to .env file

📧 **Current Behavior:**
- Emails print to console
- Verification codes work
- Ready for SMTP configuration

---

## Next Steps

1. **Choose your SMTP provider** (Resend recommended)
2. **Get credentials** (API key or app password)
3. **Configure in Supabase dashboard**
4. **Test with real email**
5. **Verify delivery and appearance**

Need help? Check:
- Supabase Docs: https://supabase.com/docs/guides/auth/auth-smtp
- Resend Docs: https://resend.com/docs
- This repo's email service code: `webapp/services/email_service.py`
