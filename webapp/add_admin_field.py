"""
Migration script to add is_admin field to users table
Default credentials: admin@smartapply.com / Admin@123
"""
from app import create_app
from extensions import db
from models.user import User

def add_admin_field():
    app = create_app()

    with app.app_context():
        # Add column using raw SQL
        try:
            db.session.execute(db.text('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE'))
            db.session.commit()
            print("[OK] Added is_admin column to users table")
        except Exception as e:
            if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                print("[OK] is_admin column already exists")
                db.session.rollback()
            else:
                print(f"[ERROR] Error adding column: {e}")
                db.session.rollback()
                return

        # Create default admin user if not exists
        admin = User.query.filter_by(email='admin@smartapply.com').first()
        if not admin:
            admin = User(
                email='admin@smartapply.com',
                username='admin',
                full_name='System Administrator',
                is_admin=True,
                is_active=True,
                email_verified=True
            )
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Created default admin user:")
            print("  Email: admin@smartapply.com")
            print("  Password: Admin@123")
        else:
            # Update existing admin to have admin rights and password
            admin.is_admin = True
            admin.email_verified = True
            admin.is_active = True
            # Set password if not already set
            if not admin.password_hash:
                admin.set_password('Admin@123')
                print("[OK] Set password for existing admin user")
            db.session.commit()
            print("[OK] Updated existing admin user with admin rights")

        print("\n[OK] Migration completed successfully!")
        print("\nDefault Admin Credentials:")
        print("  Email: admin@smartapply.com")
        print("  Password: Admin@123")

if __name__ == '__main__':
    add_admin_field()
