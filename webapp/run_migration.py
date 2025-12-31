"""
Run database migration to add profile fields
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
    """Add new profile fields to users table"""
    app = create_app()

    with app.app_context():
        try:
            print("Starting database migration...")

            # PostgreSQL migration
            migrations = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS date_of_birth DATE;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(20);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS country VARCHAR(100);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(50);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_completed BOOLEAN DEFAULT FALSE;"
            ]

            with db.engine.begin() as conn:
                for migration in migrations:
                    print(f"Executing: {migration}")
                    conn.execute(text(migration))
                    print("  [OK] Success")

            print("\n[SUCCESS] Migration completed successfully!")
            print("New columns added:")
            print("  - date_of_birth (DATE)")
            print("  - gender (VARCHAR(20))")
            print("  - country (VARCHAR(100))")
            print("  - language (VARCHAR(50))")
            print("  - profile_completed (BOOLEAN)")

        except Exception as e:
            print(f"\n[ERROR] Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    run_migration()
