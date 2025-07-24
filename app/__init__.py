"""
Wiki Veloz Fibra - Application Factory
Modular Flask application with blueprints
"""

import logging
import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Factory function to create Flask application."""
    app = Flask(__name__)

    # Basic configurations
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
    
    # Upload configurations
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Configure CORS
    CORS(app)

    # Configure login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register context processors
    register_context_processors(app)

    # Register user loader
    register_user_loader(login_manager)

    logger.info("Flask application created successfully")
    return app


def register_blueprints(app):
    """Register all application blueprints."""
    try:
        # Register main module
        from app.modules.main.routes import main_bp
        app.register_blueprint(main_bp)
        logger.info("Main blueprint registered")
    except Exception as e:
        logger.error(f"Error registering main blueprint: {e}")

    try:
        # Register auth module
        from app.modules.auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/auth")
        logger.info("Auth blueprint registered")
    except Exception as e:
        logger.error(f"Error registering auth blueprint: {e}")

    try:
        # Register users module
        from app.modules.users.routes import users_bp
        app.register_blueprint(users_bp, url_prefix="/api/users")
        logger.info("Users blueprint registered")
    except Exception as e:
        logger.error(f"Error registering users blueprint: {e}")

    try:
        # Register pages module
        from app.modules.pages.routes import pages_bp
        app.register_blueprint(pages_bp, url_prefix="/api/pages")
        logger.info("Pages blueprint registered")
    except Exception as e:
        logger.error(f"Error registering pages blueprint: {e}")

    try:
        # Register documents module
        from app.modules.documents.routes import documents_bp
        app.register_blueprint(documents_bp, url_prefix="/api/documents")
        logger.info("Documents blueprint registered")
    except Exception as e:
        logger.error(f"Error registering documents blueprint: {e}")

    try:
        # Register pdfs module
        from app.modules.pdfs.routes import pdfs_bp
        app.register_blueprint(pdfs_bp, url_prefix="/api/pdfs")
        logger.info("PDFs blueprint registered")
    except Exception as e:
        logger.error(f"Error registering pdfs blueprint: {e}")

    try:
        # Register notifications module
        from app.modules.notifications.routes import notifications_bp
        app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
        logger.info("Notifications blueprint registered")
    except Exception as e:
        logger.error(f"Error registering notifications blueprint: {e}")

    try:
        # Register analytics module
        from app.modules.analytics.routes import analytics_bp
        app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
        logger.info("Analytics blueprint registered")
    except Exception as e:
        logger.error(f"Error registering analytics blueprint: {e}")

    try:
        # Register backup module
        from app.modules.backup.routes import backup_bp
        app.register_blueprint(backup_bp, url_prefix="/api/backup")
        logger.info("Backup blueprint registered")
    except Exception as e:
        logger.error(f"Error registering backup blueprint: {e}")

    logger.info("All blueprints registered")


def register_user_loader(login_manager):
    """Register user loader for Flask-Login"""
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.auth.repositories.user_repository import UserRepository
        from app.modules.auth.models.user import User
        
        user_repo = UserRepository()
        user_data = user_repo.get_user_by_id(user_id)
        
        if user_data:
            return User(
                user_data["id"],
                user_data["username"],
                user_data["name"],
                user_data["role"],
                user_data["created_at"],
            )
        return None


def register_error_handlers(app):
    """Register custom error handlers."""

    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Page not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    logger.info("Error handlers registered")


def register_context_processors(app):
    """Register context processors for global variables."""

    @app.context_processor
    def inject_globals():
        return {"app_name": "Wiki Veloz Fibra", "app_version": "1.0.0"}

    logger.info("Context processors registered")


# Application instance for direct use
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
