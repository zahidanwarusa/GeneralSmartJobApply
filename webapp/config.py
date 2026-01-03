import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'smartapply.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy connection pooling and stability settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,                    # Number of connections to maintain
        'pool_recycle': 3600,               # Recycle connections after 1 hour
        'pool_pre_ping': True,              # Verify connections before using them
        'max_overflow': 20,                 # Maximum overflow connections
        'pool_timeout': 30,                 # Timeout for getting connection from pool
        'connect_args': {
            'connect_timeout': 10,          # Connection timeout
            'keepalives': 1,                # Enable TCP keepalives
            'keepalives_idle': 30,          # Seconds before sending keepalive
            'keepalives_interval': 10,      # Interval between keepalives
            'keepalives_count': 5           # Number of keepalives before giving up
        }
    }

    # Session configuration
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Application configuration
    ITEMS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
