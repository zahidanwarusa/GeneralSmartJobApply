"""
Database migration to add password reset fields to users table
"""
from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Password Reset Fields Migration")
    print("=" * 60)

    try:
        # Check if columns already exist
        result = db.session.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users'
            AND column_name IN ('reset_token', 'reset_token_expires')
        """))
        existing_columns = [row[0] for row in result]

        if 'reset_token' in existing_columns and 'reset_token_expires' in existing_columns:
            print("\n[INFO] Password reset fields already exist in users table")
            print("No migration needed")
        else:
            print("\n[MIGRATING] Adding password reset fields to users table...")

            # Add reset_token column if it doesn't exist
            if 'reset_token' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN reset_token VARCHAR(100)
                """))
                print("  [OK] Added reset_token column")

            # Add reset_token_expires column if it doesn't exist
            if 'reset_token_expires' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN reset_token_expires TIMESTAMP
                """))
                print("  [OK] Added reset_token_expires column")

            db.session.commit()
            print("\n[SUCCESS] Migration completed successfully!")

        # Verify the columns exist
        print("\n[VERIFYING] Checking users table structure...")
        result = db.session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name='users'
            AND column_name IN ('reset_token', 'reset_token_expires')
            ORDER BY column_name
        """))

        print("\nPassword reset columns:")
        for row in result:
            print(f"  - {row[0]} ({row[1]}) - Nullable: {row[2]}")

        print("\n" + "=" * 60)
        print("Migration complete! Password reset is now functional.")
        print("=" * 60)

    except Exception as e:
        db.session.rollback()
        print(f"\n[ERROR] Migration failed: {str(e)}")
        print("\nPlease check:")
        print("1. Database connection is working")
        print("2. You have permission to ALTER TABLE")
        print("3. The users table exists")
        raise
