"""
Database migration: Add profile fields to User model
Run this script to add new fields to existing users table
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from sqlalchemy import text
from flask import Flask

# Create minimal Flask app for migration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartapply.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def migrate():
    """Add new profile fields to users table"""
    with app.app_context():
        try:
            # Add new columns to users table
            with db.engine.connect() as conn:
                # Check if columns already exist
                result = conn.execute(text("PRAGMA table_info(users)"))
                existing_columns = {row[1] for row in result}

                migrations = []

                if 'date_of_birth' not in existing_columns:
                    migrations.append("ALTER TABLE users ADD COLUMN date_of_birth DATE")

                if 'gender' not in existing_columns:
                    migrations.append("ALTER TABLE users ADD COLUMN gender VARCHAR(20)")

                if 'country' not in existing_columns:
                    migrations.append("ALTER TABLE users ADD COLUMN country VARCHAR(100)")

                if 'language' not in existing_columns:
                    migrations.append("ALTER TABLE users ADD COLUMN language VARCHAR(50)")

                if 'profile_completed' not in existing_columns:
                    migrations.append("ALTER TABLE users ADD COLUMN profile_completed BOOLEAN DEFAULT 0")

                # Execute migrations
                for migration in migrations:
                    conn.execute(text(migration))
                    conn.commit()
                    print(f"✓ Executed: {migration}")

                if not migrations:
                    print("✓ All columns already exist. No migration needed.")
                else:
                    print(f"\n✓ Successfully added {len(migrations)} new column(s) to users table")

        except Exception as e:
            print(f"✗ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    print("Starting database migration...")
    migrate()
    print("Migration complete!")
