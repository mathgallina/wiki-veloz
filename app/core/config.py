"""
Configuration management for Wiki Veloz
CDD v2.0 - Centralized configuration
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Upload Configuration
    UPLOAD_FOLDER = "app/static/uploads"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt", "jpg", "jpeg", "png", "gif"}
    
    # Database Configuration
    DATA_FOLDER = "app/data"
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS_FILE = os.environ.get(
        "GOOGLE_DRIVE_CREDENTIALS_FILE"
    )
    GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    
    # Backup Configuration
    BACKUP_FOLDER = "backups"
    BACKUP_RETENTION_DAYS = 30
    
    # Notification Configuration
    NOTIFICATION_RETENTION_DAYS = 30
    
    # Analytics Configuration
    ANALYTICS_ENABLED = True
    ACTIVITY_LOG_RETENTION = 1000


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATA_FOLDER = "tests/test_data"


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
