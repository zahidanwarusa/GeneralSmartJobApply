"""
Create all database tables for the application
Run this if you get "relation does not exist" errors
"""
from app import create_app
from extensions import db
from models.user import User, JobDescription, Resume, Application

def create_all_tables():
    """Create all database tables"""
    app = create_app()

    with app.app_context():
        try:
            # Create all tables defined in models
            db.create_all()
            print("[OK] All database tables created successfully!")
            print("\nTables created:")
            print("  - users")
            print("  - job_descriptions")
            print("  - resumes")
            print("  - applications")

            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\nVerified tables in database: {', '.join(tables)}")

        except Exception as e:
            print(f"[ERROR] Failed to create tables: {e}")
            return False

    return True

if __name__ == '__main__':
    create_all_tables()
