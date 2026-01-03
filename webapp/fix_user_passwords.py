"""
Fix users with null password_hash
Sets Admin@123 for admin, prompts to set password for other users
"""
from app import create_app
from extensions import db
from models.user import User

def fix_passwords():
    """Fix users with null passwords"""
    app = create_app()

    with app.app_context():
        # Find users with null passwords
        users_without_password = User.query.filter(
            (User.password_hash == None) | (User.password_hash == '')
        ).all()

        if not users_without_password:
            print("[OK] All users have passwords set!")
            return

        print(f"Found {len(users_without_password)} user(s) without password:\n")

        for user in users_without_password:
            print(f"User: {user.username} ({user.email})")

            if user.email == 'admin@smartapply.com':
                # Auto-set admin password
                user.set_password('Admin@123')
                user.is_admin = True
                user.email_verified = True
                user.is_active = True
                print(f"  -> Set password: Admin@123")
            else:
                # Set a default password for other users
                default_password = 'TempPass@123'
                user.set_password(default_password)
                user.email_verified = True
                user.is_active = True
                print(f"  -> Set temporary password: {default_password}")
                print(f"  -> User should change this on first login")

        db.session.commit()
        print("\n[OK] All passwords fixed!")
        print("\nAdmin Login:")
        print("  Email: admin@smartapply.com")
        print("  Password: Admin@123")

if __name__ == '__main__':
    fix_passwords()
