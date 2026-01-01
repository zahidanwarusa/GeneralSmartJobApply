"""
Test password reset flow
"""
from app import create_app
from extensions import db
from models.user import User
from services.email_service import EmailService
from flask import url_for

app = create_app()
email_service = EmailService()

with app.app_context():
    print("=" * 60)
    print("Password Reset Flow Test")
    print("=" * 60)

    # Test with existing user
    user = User.query.filter_by(email='zahidsdet@gmail.com').first()

    if not user:
        print("\n[ERROR] User zahidsdet@gmail.com not found")
        print("Please create a user first or update the email in this script")
        exit(1)

    print(f"\n[TEST] Testing password reset for: {user.email}")
    print(f"Current password hash exists: {bool(user.password_hash)}")

    # Step 1: Generate reset token
    print("\n[STEP 1] Generating reset token...")
    token = user.generate_reset_token()
    db.session.commit()
    print(f"  Token generated: {token[:20]}...")
    print(f"  Token expires: {user.reset_token_expires}")

    # Step 2: Create reset link
    print("\n[STEP 2] Creating reset link...")
    with app.test_request_context():
        reset_link = url_for('auth.reset_password', token=token, _external=True)
    print(f"  Reset link: {reset_link}")

    # Step 3: Send email
    print("\n[STEP 3] Sending password reset email...")
    result = email_service.send_password_reset(user.email, reset_link)

    if result['success']:
        print(f"  [OK] Email sent via {result.get('provider', 'console')}")
        if result.get('provider') == 'resend':
            print(f"  Check your inbox at {user.email}")
        else:
            print(f"  Email details printed to console above")
    else:
        print(f"  [ERROR] Failed to send email: {result.get('message')}")

    # Step 4: Verify token
    print("\n[STEP 4] Verifying token...")
    if user.verify_reset_token(token):
        print(f"  [OK] Token is valid")
    else:
        print(f"  [ERROR] Token is invalid or expired")

    # Step 5: Simulate password reset
    print("\n[STEP 5] Simulating password reset...")
    old_hash = user.password_hash
    test_password = "NewTestPassword123!"
    user.reset_password(test_password)
    db.session.commit()

    print(f"  [OK] Password reset successful")
    print(f"  Old hash: {old_hash[:30]}...")
    print(f"  New hash: {user.password_hash[:30]}...")
    print(f"  Reset token cleared: {user.reset_token is None}")

    # Step 6: Verify new password works
    print("\n[STEP 6] Verifying new password...")
    if user.check_password(test_password):
        print(f"  [OK] New password verified successfully")
    else:
        print(f"  [ERROR] Password verification failed")

    print("\n" + "=" * 60)
    print("Password Reset Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check your email inbox (if using Resend)")
    print("2. Click the reset link or copy it from console")
    print("3. Enter your new password on the web interface")
    print(f"\nReset link: {reset_link}")
    print(f"Test password used: {test_password}")
    print("=" * 60)
