from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    supabase_user_id = db.Column(db.String(255), unique=True, index=True)  # UUID from Supabase Auth
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users

    # Profile information
    full_name = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)  # male, female, other, prefer_not_to_say
    country = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True)  # Path to profile picture
    profile_completed = db.Column(db.Boolean, default=False)  # Track if onboarding is complete

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expires = db.Column(db.DateTime, nullable=True)

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
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def has_password(self):
        """Check if user has a password set (False for OAuth users)"""
        return self.password_hash is not None and self.password_hash != ''

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.verification_code = code
        self.verification_code_expires = datetime.utcnow() + timedelta(minutes=15)
        return code

    def verify_code(self, code):
        """Verify if the provided code matches and is not expired"""
        if not self.verification_code or not self.verification_code_expires:
            return False
        if datetime.utcnow() > self.verification_code_expires:
            return False
        return self.verification_code == code

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
