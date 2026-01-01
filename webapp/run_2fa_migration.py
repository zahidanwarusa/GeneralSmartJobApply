"""
Database migration to add 2FA fields to users table
"""
from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Two-Factor Authentication (2FA) Migration")
    print("=" * 60)

    try:
        # Check if columns already exist
        result = db.session.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users'
            AND column_name IN ('two_factor_enabled', 'two_factor_secret', 'backup_codes')
        """))
        existing_columns = [row[0] for row in result]

        if len(existing_columns) == 3:
            print("\n[INFO] 2FA fields already exist in users table")
            print("No migration needed")
        else:
            print("\n[MIGRATING] Adding 2FA fields to users table...")

            # Add two_factor_enabled column if it doesn't exist
            if 'two_factor_enabled' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN two_factor_enabled BOOLEAN DEFAULT FALSE
                """))
                print("  [OK] Added two_factor_enabled column")

            # Add two_factor_secret column if it doesn't exist
            if 'two_factor_secret' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN two_factor_secret VARCHAR(32)
                """))
                print("  [OK] Added two_factor_secret column")

            # Add backup_codes column if it doesn't exist
            if 'backup_codes' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN backup_codes TEXT
                """))
                print("  [OK] Added backup_codes column")

            db.session.commit()
            print("\n[SUCCESS] Migration completed successfully!")

        # Verify the columns exist
        print("\n[VERIFYING] Checking users table structure...")
        result = db.session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name='users'
            AND column_name IN ('two_factor_enabled', 'two_factor_secret', 'backup_codes')
            ORDER BY column_name
        """))

        print("\n2FA columns:")
        for row in result:
            print(f"  - {row[0]} ({row[1]}) - Nullable: {row[2]}")

        print("\n" + "=" * 60)
        print("Migration complete! 2FA fields are ready.")
        print("=" * 60)
        print("\nNext steps:")
        print("1. See COMPLETE_2FA_IMPLEMENTATION.md for implementation plan")
        print("2. Run: python app.py")
        print("3. Access 2FA setup in user settings (coming soon)")
        print("=" * 60)

    except Exception as e:
        db.session.rollback()
        print(f"\n[ERROR] Migration failed: {str(e)}")
        print("\nPlease check:")
        print("1. Database connection is working")
        print("2. You have permission to ALTER TABLE")
        print("3. The users table exists")
        raise
