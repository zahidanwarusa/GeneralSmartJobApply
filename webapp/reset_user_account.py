"""
Reset user account - deletes from both Flask DB and optionally Supabase Auth
"""
from extensions import db
from models.user import User
from app import create_app
import os

app = create_app()

print("=" * 60)
print("User Account Reset Tool")
print("=" * 60)

with app.app_context():
    # Check current users
    all_users = User.query.all()

    print(f"\nCurrent users in database ({len(all_users)}):")
    for idx, user in enumerate(all_users, 1):
        print(f"{idx}. {user.email} (verified: {user.email_verified}, username: {user.username})")

    if not all_users:
        print("No users found in database.")
        exit()

    # Ask which user to delete
    email_to_delete = input("\nEnter email to delete (or 'all' to delete all): ").strip()

    if email_to_delete.lower() == 'all':
        confirm = input("Are you sure you want to delete ALL users? (yes/no): ").strip().lower()
        if confirm == 'yes':
            for user in all_users:
                db.session.delete(user)
            db.session.commit()
            print(f"\n[SUCCESS] Deleted all {len(all_users)} users")
        else:
            print("Cancelled")
    else:
        user = User.query.filter_by(email=email_to_delete).first()
        if user:
            print(f"\nDeleting user:")
            print(f"  Email: {user.email}")
            print(f"  Username: {user.username}")
            print(f"  Created: {user.created_at}")
            print(f"  Email verified: {user.email_verified}")

            confirm = input("\nConfirm deletion? (yes/no): ").strip().lower()
            if confirm == 'yes':
                db.session.delete(user)
                db.session.commit()
                print(f"\n[SUCCESS] User {email_to_delete} deleted from Flask database")

                print("\nNOTE: If this user also exists in Supabase Auth:")
                print("1. Go to: https://supabase.com/dashboard")
                print("2. Select your project")
                print("3. Authentication → Users")
                print("4. Find and delete the user there too")
            else:
                print("Cancelled")
        else:
            print(f"\n[ERROR] No user found with email: {email_to_delete}")

    # Show remaining users
    remaining = User.query.all()
    print(f"\nRemaining users: {len(remaining)}")
    for user in remaining:
        print(f"  - {user.email}")
