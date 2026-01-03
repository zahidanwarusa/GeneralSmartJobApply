"""
Admin model - separate table for administrators
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Admin(UserMixin, db.Model):
    """Admin model for system administrators"""

    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile information
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(50), default='admin')  # admin, super_admin, moderator

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=True)

    # Permissions
    can_manage_users = db.Column(db.Boolean, default=True)
    can_manage_payments = db.Column(db.Boolean, default=True)
    can_view_analytics = db.Column(db.Boolean, default=True)
    can_manage_system = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Hash and set the admin's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    @property
    def is_admin(self):
        """Always True for admin model"""
        return True

    @property
    def is_super_admin(self):
        """Check if super admin"""
        return self.role == 'super_admin'

    def __repr__(self):
        return f'<Admin {self.username}>'
