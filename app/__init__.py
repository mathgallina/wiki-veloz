"""
Wiki Veloz Fibra - Application Factory
Simplified version for Render deployment
"""

import logging
import os

from flask import Flask
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Factory function to create Flask application."""
    app = Flask(__name__)

    # Basic configurations
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # Configure login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "info"

    # Register blueprints (simplified)
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register context processors
    register_context_processors(app)

    logger.info("Flask application created successfully")
    return app


def register_blueprints(app):
    """Register all application blueprints."""
    try:
        # Register documents module
        from app.modules.documents.routes import documents_bp
        app.register_blueprint(documents_bp)
        logger.info("Documents blueprint registered")
    except Exception as e:
        logger.error(f"Error registering documents blueprint: {e}")

    try:
        # Register other modules as needed
        from app.modules.users.routes import users_bp
        app.register_blueprint(users_bp)
        logger.info("Users blueprint registered")
    except Exception as e:
        logger.error(f"Error registering users blueprint: {e}")

    logger.info("Blueprints registered")


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
