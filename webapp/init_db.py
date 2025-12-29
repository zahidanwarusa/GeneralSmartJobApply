"""Database initialization script"""
from app import create_app
from extensions import db
from models.user import User, JobDescription, Resume, Application

def init_database():
    """Initialize the database with tables"""
    app = create_app()

    with app.app_context():
        # Drop all tables (caution: this will delete all data)
        print("Dropping all tables...")
        db.drop_all()

        # Create all tables
        print("Creating all tables...")
        db.create_all()

        print("[SUCCESS] Database initialized successfully!")
        print(f"[SUCCESS] Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")

        # Create a test user (optional)
        create_test = input("\nCreate a test user? (y/n): ").lower()
        if create_test == 'y':
            test_user = User(
                email='test@example.com',
                username='testuser',
                full_name='Test User'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print("[SUCCESS] Test user created:")
            print("  Email: test@example.com")
            print("  Password: password123")

if __name__ == '__main__':
    init_database()
