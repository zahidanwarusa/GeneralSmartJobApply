from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile information
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    job_descriptions = db.relationship('JobDescription', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    resumes = db.relationship('Resume', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

class JobDescription(db.Model):
    """Job description model"""

    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.String(64), unique=True, nullable=False, index=True)

    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string

    # Source information
    source_type = db.Column(db.String(20))  # 'text', 'url', 'file'
    source_url = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resumes = db.relationship('Resume', backref='job', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='job', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<JobDescription {self.title} at {self.company}>'

class Resume(db.Model):
    """Resume model"""

    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'))

    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(10))  # 'docx', 'pdf'

    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    error_message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Resume {self.title}>'

class Application(db.Model):
    """Application tracking model"""

    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

    # Application details
    status = db.Column(db.String(20), default='applied')  # applied, interview, offer, rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    # Follow-up tracking
    last_followup = db.Column(db.DateTime)
    next_followup = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Application {self.id} - {self.status}>'
