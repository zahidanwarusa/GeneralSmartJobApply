"""
Fix database schema to match current models
Adds missing columns to existing tables
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def fix_schema():
    """Add missing columns to database tables"""
    app = create_app()

    with app.app_context():
        print("Checking and fixing database schema...")

        # Get inspector to check existing columns
        inspector = db.inspect(db.engine)

        # Fix resumes table
        if 'resumes' in inspector.get_table_names():
            existing_columns = [col['name'] for col in inspector.get_columns('resumes')]
            print(f"\nResumes table existing columns: {existing_columns}")

            # Add missing columns
            columns_to_add = {
                'job_id': 'INTEGER',
                'file_path': 'VARCHAR(500)',
                'file_type': 'VARCHAR(10)',
                'status': "VARCHAR(20) DEFAULT 'completed'",
                'error_message': 'TEXT',
                'completed_at': 'TIMESTAMP'
            }

            for col_name, col_type in columns_to_add.items():
                if col_name not in existing_columns:
                    try:
                        db.session.execute(text(f'ALTER TABLE resumes ADD COLUMN {col_name} {col_type}'))
                        db.session.commit()
                        print(f"[OK] Added {col_name} column to resumes table")
                    except Exception as e:
                        db.session.rollback()
                        print(f"[INFO] Column {col_name} may already exist or error: {e}")

            # Add foreign key constraint if needed
            if 'job_id' in [col_name for col_name, _ in columns_to_add.items()]:
                try:
                    db.session.execute(text('ALTER TABLE resumes ADD CONSTRAINT fk_resumes_job_id FOREIGN KEY (job_id) REFERENCES job_descriptions(id)'))
                    db.session.commit()
                    print("[OK] Added foreign key constraint for job_id")
                except Exception as e:
                    db.session.rollback()
                    if 'already exists' not in str(e).lower():
                        print(f"[INFO] Foreign key constraint: {e}")

        # Fix applications table
        if 'applications' in inspector.get_table_names():
            existing_columns = [col['name'] for col in inspector.get_columns('applications')]
            print(f"\nApplications table existing columns: {existing_columns}")

            if 'job_id' not in existing_columns:
                try:
                    db.session.execute(text('ALTER TABLE applications ADD COLUMN job_id INTEGER'))
                    db.session.execute(text('ALTER TABLE applications ADD CONSTRAINT fk_applications_job_id FOREIGN KEY (job_id) REFERENCES job_descriptions(id)'))
                    db.session.commit()
                    print("[OK] Added job_id column to applications table")
                except Exception as e:
                    db.session.rollback()
                    print(f"[ERROR] Could not add job_id to applications: {e}")
            else:
                print("[OK] job_id already exists in applications table")

            if 'resume_id' not in existing_columns:
                try:
                    db.session.execute(text('ALTER TABLE applications ADD COLUMN resume_id INTEGER'))
                    db.session.execute(text('ALTER TABLE applications ADD CONSTRAINT fk_applications_resume_id FOREIGN KEY (resume_id) REFERENCES resumes(id)'))
                    db.session.commit()
                    print("[OK] Added resume_id column to applications table")
                except Exception as e:
                    db.session.rollback()
                    print(f"[ERROR] Could not add resume_id to applications: {e}")
            else:
                print("[OK] resume_id already exists in applications table")

        print("\n[OK] Schema fix completed!")
        print("\nYou can now restart your application.")

if __name__ == '__main__':
    fix_schema()
