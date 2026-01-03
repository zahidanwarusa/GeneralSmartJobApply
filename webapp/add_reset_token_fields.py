"""
Migration script to add password reset token fields to users table
Run this script to update your database schema
"""
import sys
import os

# Add the webapp directory to the Python path FIRST
current_dir = os.path.dirname(os.path.abspath(__file__))
# Insert at the very beginning to override other paths
sys.path.insert(0, current_dir)

# Set environment variable for Flask
os.environ.setdefault('FLASK_APP', 'app.py')

from app import create_app
from extensions import db
from sqlalchemy import text

def add_reset_token_fields():
    """Add reset_token and reset_token_expires columns to users table"""
    app = create_app()

    with app.app_context():
        print("Starting database migration...")
        print("Adding password reset token fields to users table...")

        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]

            if 'reset_token' in columns and 'reset_token_expires' in columns:
                print("✓ Password reset token fields already exist. No migration needed.")
                return

            # Add the columns
            with db.engine.connect() as conn:
                if 'reset_token' not in columns:
                    print("  - Adding reset_token column...")
                    conn.execute(text('ALTER TABLE users ADD COLUMN reset_token VARCHAR(100) UNIQUE'))
                    conn.commit()
                    print("    ✓ reset_token column added")

                if 'reset_token_expires' not in columns:
                    print("  - Adding reset_token_expires column...")
                    conn.execute(text('ALTER TABLE users ADD COLUMN reset_token_expires DATETIME'))
                    conn.commit()
                    print("    ✓ reset_token_expires column added")

            print("\n✓ Migration completed successfully!")
            print("  Password reset functionality is now enabled.")

        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            print("\nPlease ensure:")
            print("  1. The database is accessible")
            print("  2. You have the necessary permissions")
            print("  3. The users table exists")
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("Password Reset Token Fields Migration")
    print("=" * 60)
    print()

    try:
        add_reset_token_fields()
        print()
        print("=" * 60)
        print("Migration script completed successfully!")
        print("=" * 60)
    except Exception as e:
        print()
        print("=" * 60)
        print("Migration script failed!")
        print("=" * 60)
        sys.exit(1)
