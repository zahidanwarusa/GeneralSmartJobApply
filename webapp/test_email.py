"""
Quick test script for email service
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Import email service
from services.email_service import EmailService

# Initialize service
email_service = EmailService()

# Test sending verification code
test_email = input("Enter your email address to test: ")
test_code = "123456"

print(f"\n[TEST] Attempting to send verification email to {test_email}...")
result = email_service.send_verification_code(test_email, test_code)

print(f"\n[TEST] Result: {result}")

if result['success']:
    print(f"✅ Email sent successfully via {result.get('provider', 'unknown')}")
    print(f"\nCheck your inbox at {test_email}")
else:
    print(f"❌ Failed to send email: {result.get('message')}")
