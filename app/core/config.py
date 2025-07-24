"""
Configuration settings for Wiki Veloz
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Upload settings
    UPLOAD_FOLDER = "app/static/uploads"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt", "jpg", "jpeg", "png", "gif"}
    
    # Database settings
    DATA_FOLDER = "app/data"
    
    # Session settings
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Logging settings
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    
    # Backup settings
    BACKUP_FOLDER = "backups"
    MAX_BACKUPS = 10
    
    # Google Drive settings
    GOOGLE_DRIVE_CREDENTIALS_FILE = "credentials.json"
    GOOGLE_DRIVE_TOKEN_FILE = "token.json"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
