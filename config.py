import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-recruitment-secret-key-2026')
    
    # Primary MySQL with automatic SQLite fallback
    mysql_host = os.getenv('MYSQL_HOST', 'localhost')
    mysql_port = os.getenv('MYSQL_PORT', '3306')
    mysql_user = os.getenv('MYSQL_USER', '')
    mysql_password = os.getenv('MYSQL_PASSWORD', '')
    mysql_db = os.getenv('MYSQL_DATABASE', 'intelligent_recruitment')
    
    default_sqlite = f"sqlite:///{BASE_DIR / 'recruitment.db'}"
    
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    elif mysql_user and mysql_db:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
    else:
        SQLALCHEMY_DATABASE_URI = default_sqlite

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Cookie Configuration for iFrame & HTTPS Support
    SESSION_COOKIE_NAME = 'recruit360_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_PARTITIONED = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE = True
    
    # File Uploads
    UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)) # 16 MB max
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # External API Tokens (Optional)
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME', '')
    KAGGLE_KEY = os.getenv('KAGGLE_KEY', '')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = BASE_DIR / 'test_uploads'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_SAMESITE = 'Lax'
