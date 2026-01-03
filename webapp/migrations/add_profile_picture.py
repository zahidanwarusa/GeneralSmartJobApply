"""
Migration script to add profile_picture field to users table
Run this script to update the database schema
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from app import create_app

def add_profile_picture_field():
    """Add profile_picture column to users table"""
    app = create_app()
    with app.app_context():
        try:
            # Add the column using raw SQL to avoid model conflicts
            with db.engine.connect() as connection:
                connection.execute(db.text(
                    "ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"
                ))
                connection.commit()
            print("[SUCCESS] Successfully added profile_picture field to users table")
        except Exception as e:
            print(f"[WARNING] Migration may have already been applied or error occurred: {e}")

if __name__ == '__main__':
    add_profile_picture_field()
