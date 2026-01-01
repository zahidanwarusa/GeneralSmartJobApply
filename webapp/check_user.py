"""Check user verification status"""
from extensions import db
from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    # Check for user
    user = User.query.filter_by(email='zahidsdet@gmail.com').first()

    if user:
        print(f"[OK] User found: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  Email verified: {user.email_verified}")
        print(f"  Verification code: {user.verification_code or 'None'}")
        print(f"  Code expires: {user.verification_code_expires or 'None'}")
        print(f"  Created: {user.created_at}")

        if user.verification_code:
            from datetime import datetime
            if user.verification_code_expires and datetime.utcnow() < user.verification_code_expires:
                print(f"\n  [OK] Code is VALID and not expired")
            else:
                print(f"\n  [ERROR] Code is EXPIRED")
    else:
        print("[ERROR] No user found with email: zahidsdet@gmail.com")
        print("\nAll users in database:")
        all_users = User.query.all()
        for u in all_users:
            print(f"  - {u.email} (verified: {u.email_verified})")
