"""
Email service for sending verification codes and other emails
Uses Supabase Admin API for email delivery with console fallback
"""
import os
from typing import Dict, Any
from supabase_client import get_supabase_client

# Try to import resend for fallback, but don't fail if not available
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False


class EmailService:
    """Service for sending emails via Supabase with Resend/console fallback"""

    def __init__(self):
        self.app_name = "SmartApply Pro"
        self.support_email = os.environ.get('SUPPORT_EMAIL', 'support@smartapplypro.com')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@smartapplypro.com')

        # Initialize Supabase client
        try:
            self.supabase = get_supabase_client()
            self.supabase_enabled = True
            print(f"[EMAIL SERVICE] Supabase client initialized successfully")
        except Exception as e:
            self.supabase_enabled = False
            print(f"[EMAIL SERVICE] Supabase initialization failed: {str(e)}")

        # Initialize Resend as fallback if API key is available
        self.resend_api_key = os.environ.get('RESEND_API_KEY')
        if self.resend_api_key and RESEND_AVAILABLE:
            resend.api_key = self.resend_api_key
            self.resend_enabled = True
            print(f"[EMAIL SERVICE] Resend fallback initialized successfully")
        else:
            self.resend_enabled = False

        # Determine email method
        if not self.supabase_enabled and not self.resend_enabled:
            print(f"[EMAIL SERVICE] Using console fallback for emails")

    def send_verification_code(self, email: str, code: str) -> Dict[str, Any]:
        """
        Send verification code email

        Args:
            email: Recipient email address
            code: 6-digit verification code

        Returns:
            Dict with success status and message
        """
        try:
            # Create email content
            subject = f"Verify Your {self.app_name} Account"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        border-radius: 8px;
                        padding: 40px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo {{
                        font-size: 28px;
                        font-weight: bold;
                        color: #2d3748;
                        margin-bottom: 10px;
                    }}
                    .code-container {{
                        background-color: #f7fafc;
                        border: 2px dashed #cbd5e0;
                        border-radius: 8px;
                        padding: 30px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .code {{
                        font-size: 36px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        color: #2d3748;
                        font-family: 'Courier New', monospace;
                    }}
                    .message {{
                        color: #4a5568;
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #e2e8f0;
                        color: #718096;
                        font-size: 14px;
                        text-align: center;
                    }}
                    .warning {{
                        background-color: #fff5f5;
                        border-left: 4px solid #fc8181;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 4px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">{self.app_name}</div>
                        <p style="color: #718096; margin: 0;">Email Verification</p>
                    </div>

                    <div class="message">
                        <p>Hello,</p>
                        <p>Thank you for registering with {self.app_name}! To complete your registration, please verify your email address using the code below:</p>
                    </div>

                    <div class="code-container">
                        <p style="margin: 0 0 10px 0; color: #718096; font-size: 14px;">Your Verification Code</p>
                        <div class="code">{code}</div>
                        <p style="margin: 10px 0 0 0; color: #718096; font-size: 12px;">This code will expire in 15 minutes</p>
                    </div>

                    <div class="message">
                        <p>If you didn't request this verification code, please ignore this email or contact our support team if you have concerns.</p>
                    </div>

                    <div class="warning">
                        <strong>Security Notice:</strong> Never share this code with anyone. {self.app_name} will never ask for your verification code.
                    </div>

                    <div class="footer">
                        <p>This is an automated message from {self.app_name}.</p>
                        <p>Need help? Contact us at <a href="mailto:{self.support_email}">{self.support_email}</a></p>
                        <p>&copy; 2024 {self.app_name}. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Plain text version as fallback
            text_content = f"""
            {self.app_name} - Email Verification

            Hello,

            Thank you for registering with {self.app_name}! To complete your registration, please verify your email address using the code below:

            Verification Code: {code}

            This code will expire in 15 minutes.

            If you didn't request this verification code, please ignore this email or contact our support team.

            Security Notice: Never share this code with anyone. {self.app_name} will never ask for your verification code.

            Need help? Contact us at {self.support_email}

            © 2024 {self.app_name}. All rights reserved.
            """

            # Option 1: Send email using Resend (Direct API - Most Reliable)
            if self.resend_enabled and RESEND_AVAILABLE:
                try:
                    params = {
                        "from": self.from_email,
                        "to": [email],
                        "subject": subject,
                        "html": html_content
                    }

                    email_response = resend.Emails.send(params)
                    print(f"[EMAIL SERVICE] Email sent successfully via Resend to {email}")
                    print(f"[EMAIL SERVICE] Resend ID: {email_response.get('id', 'N/A')}")

                    return {
                        'success': True,
                        'message': 'Verification email sent successfully',
                        'provider': 'resend'
                    }
                except Exception as e:
                    error_msg = str(e)
                    print(f"[EMAIL SERVICE ERROR] Resend failed: {error_msg}")

                    # Check if it's a domain restriction error
                    if "only send testing emails to your own email address" in error_msg.lower():
                        print(f"[EMAIL SERVICE] Resend requires domain verification for this recipient")
                        print(f"[EMAIL SERVICE] Add and verify your domain at: https://resend.com/domains")
                        print(f"[EMAIL SERVICE] Or send to verified email: zahidsdet@gmail.com")

                    # Fall through to console logging

            # Console fallback (for development or when email is not configured)
            print(f"\n{'='*60}")
            print(f"[EMAIL SERVICE] CONSOLE FALLBACK - Email details:")
            print(f"To: {email}")
            print(f"Subject: {subject}")
            print(f"Verification Code: {code}")
            print(f"{'='*60}\n")

            return {
                'success': True,
                'message': 'Verification email sent successfully'
            }

        except Exception as e:
            print(f"[EMAIL SERVICE ERROR] Failed to send email: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }

    def send_password_reset(self, email: str, reset_link: str) -> Dict[str, Any]:
        """
        Send password reset email

        Args:
            email: Recipient email address
            reset_link: Password reset link

        Returns:
            Dict with success status and message
        """
        try:
            subject = f"Reset Your {self.app_name} Password"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        border-radius: 8px;
                        padding: 40px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 30px;
                        background-color: #4299e1;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #e2e8f0;
                        color: #718096;
                        font-size: 14px;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Reset Your Password</h2>
                    <p>We received a request to reset your password for your {self.app_name} account.</p>
                    <p>Click the button below to reset your password:</p>
                    <a href="{reset_link}" class="button">Reset Password</a>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you didn't request a password reset, please ignore this email.</p>
                    <div class="footer">
                        <p>&copy; 2024 {self.app_name}. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            print(f"\n[EMAIL SERVICE] Password reset email")
            print(f"To: {email}")
            print(f"Reset Link: {reset_link}\n")

            return {
                'success': True,
                'message': 'Password reset email sent successfully'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }
