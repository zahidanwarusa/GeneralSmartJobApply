"""
Create admins table and migrate existing admin users
"""
from app import create_app
from extensions import db
from models.admin import Admin
from models.user import User

def create_admin_table():
    """Create admins table and migrate admin users from users table"""
    app = create_app()

    with app.app_context():
        print("Creating admins table...")

        # Create admins table
        try:
            db.create_all()
            print("[OK] Admins table created successfully!")
        except Exception as e:
            print(f"[INFO] Table may already exist: {e}")

        # Migrate existing admin users
        print("\nMigrating admin users from users table...")
        admin_users = User.query.filter_by(is_admin=True).all()

        if not admin_users:
            print("[INFO] No admin users found in users table")
        else:
            for user in admin_users:
                # Check if admin already exists
                existing_admin = Admin.query.filter_by(email=user.email).first()
                if existing_admin:
                    print(f"[SKIP] Admin {user.email} already exists in admins table")
                    continue

                # Create new admin record
                admin = Admin(
                    email=user.email,
                    username=user.username,
                    password_hash=user.password_hash,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    email_verified=user.email_verified,
                    created_at=user.created_at,
                    last_login=user.last_login
                )

                db.session.add(admin)
                print(f"[OK] Migrated admin: {user.email}")

            db.session.commit()
            print(f"\n[OK] Migrated {len(admin_users)} admin user(s)")

        # Create default super admin if no admins exist
        if Admin.query.count() == 0:
            print("\nCreating default super admin...")
            super_admin = Admin(
                email='admin@smartapply.com',
                username='admin',
                full_name='System Administrator',
                role='super_admin',
                is_active=True,
                email_verified=True,
                can_manage_users=True,
                can_manage_payments=True,
                can_view_analytics=True,
                can_manage_system=True
            )
            super_admin.set_password('Admin@123')
            db.session.add(super_admin)
            db.session.commit()
            print("[OK] Created default super admin")
            print("  Email: admin@smartapply.com")
            print("  Password: Admin@123")

        print("\n[OK] Admin table setup completed!")
        print(f"\nTotal admins: {Admin.query.count()}")
        print(f"Total users: {User.query.count()}")

        # Show all admins
        print("\nAdmin accounts:")
        for admin in Admin.query.all():
            print(f"  - {admin.username} ({admin.email}) - Role: {admin.role}")

if __name__ == '__main__':
    create_admin_table()
