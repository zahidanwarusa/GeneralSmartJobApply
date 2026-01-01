"""Manually verify user"""
from extensions import db
from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='zahidsdet@gmail.com').first()

    if user:
        print(f"User: {user.email}")
        print(f"Current verification status: {user.email_verified}")
        print(f"Current code: {user.verification_code}")

        # Verify the code
        code_to_verify = input("\nEnter verification code: ").strip()

        if user.verify_code(code_to_verify):
            user.email_verified = True
            user.verification_code = None
            user.verification_code_expires = None
            db.session.commit()

            print("\n[SUCCESS] Email verified!")
            print(f"User {user.email} is now verified and can log in.")
        else:
            print("\n[ERROR] Invalid or expired code")
            print(f"Expected: {user.verification_code}")
    else:
        print("User not found")
