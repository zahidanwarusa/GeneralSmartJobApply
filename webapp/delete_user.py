"""Delete test user to start fresh"""
from extensions import db
from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='zahidsdet@gmail.com').first()

    if user:
        print(f"Deleting user: {user.email}")
        db.session.delete(user)
        db.session.commit()
        print("User deleted successfully!")
    else:
        print("No user found to delete")
