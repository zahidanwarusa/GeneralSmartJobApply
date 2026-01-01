"""Send a new verification code via email"""
from extensions import db
from models.user import User
from services.email_service import EmailService
from app import create_app

app = create_app()
email_service = EmailService()

with app.app_context():
    user = User.query.filter_by(email='zahidsdet@gmail.com').first()

    if user:
        # Generate new verification code
        code = user.generate_verification_code()
        db.session.commit()

        print(f"Generated new code for {user.email}: {code}")

        # Send email
        result = email_service.send_verification_code(user.email, code)

        if result['success']:
            print(f"\n[SUCCESS] Email sent via {result.get('provider', 'console')}")
            print(f"Check your inbox at {user.email}")
        else:
            print(f"\n[ERROR] Failed to send email")
    else:
        print("User not found")
