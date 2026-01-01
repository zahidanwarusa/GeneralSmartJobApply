"""
Run database migration to add email verification fields
Works with PostgreSQL database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from extensions import db
from app import create_app

def run_migration():
    """Add email verification fields to users table"""
    app = create_app()

    with app.app_context():
        try:
            print("Starting email verification migration...")

            # PostgreSQL migration
            migrations = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP;"
            ]

            with db.engine.begin() as conn:
                for migration in migrations:
                    print(f"Executing: {migration}")
                    conn.execute(text(migration))
                    print("  [OK] Success")

            print("\n[SUCCESS] Email verification migration completed successfully!")
            print("New columns added:")
            print("  - email_verified (BOOLEAN)")
            print("  - verification_code (VARCHAR(6))")
            print("  - verification_code_expires (TIMESTAMP)")

        except Exception as e:
            print(f"\n[ERROR] Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    run_migration()
