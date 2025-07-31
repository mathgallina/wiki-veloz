"""
Wiki Veloz Fibra - Application Factory
CDD v2.0 - Modular Flask application with blueprints

Este módulo contém a factory function principal para criar a aplicação Flask.
Organiza todos os blueprints, configurações e inicializações necessárias.

@author: Matheus Gallina
@version: 1.0.0
@license: MIT
"""

import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from app.core.config import config
from app.core.database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask.
    
    Esta função configura toda a aplicação, incluindo:
    - Configurações básicas do Flask
    - CORS e Login Manager
    - Registro de blueprints
    - Handlers de erro
    - Processadores de contexto
    - Inicialização de dados padrão
    
    Args:
        config_name (str, optional): Nome da configuração a ser usada.
                                   Se None, usa FLASK_ENV ou 'default'.
    
    Returns:
        Flask: Instância configurada da aplicação Flask
        
    Raises:
        Exception: Se houver erro na configuração dos blueprints
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Configure CORS
    CORS(app)
    
    # Configure login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Por favor, faça login para acessar esta página."
    )
    login_manager.login_message_category = "info"
    
    # Initialize database manager
    db_manager = DatabaseManager(config[config_name]())
    
    # Register blueprints
    register_blueprints(app, db_manager)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register context processors
    register_context_processors(app)
    
    # Register user loader
    register_user_loader(login_manager, db_manager)
    
    # Initialize default data
    initialize_default_data(db_manager)
    
    logger.info("Flask application created successfully")
    return app


def register_blueprints(app, db_manager):
    """
    Registra todos os blueprints da aplicação.
    
    Esta função registra todos os módulos da aplicação como blueprints:
    - Main: Rotas principais
    - Auth: Autenticação e login
    - Users: Gerenciamento de usuários
    - Pages: API de páginas
    - Documents: Gerenciamento de documentos
    - Backup: Sistema de backup
    - Analytics: Analytics e relatórios
    - Notifications: Sistema de notificações
    - PDFs: Gerenciamento de PDFs
    - Activity: Log de atividades
    
    Args:
        app (Flask): Instância da aplicação Flask
        db_manager (DatabaseManager): Gerenciador de banco de dados
        
    Raises:
        Exception: Se houver erro no registro de algum blueprint
    """
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
        # Also register auth blueprint for API routes without prefix
        app.register_blueprint(
            auth_bp, url_prefix="", name="auth_api"
        )
        logger.info("Auth blueprint registered")
    except Exception as e:
        logger.error(f"Error registering auth blueprint: {e}")
    
    try:
        # Register users module
        from app.modules.users.routes import users_bp
        app.register_blueprint(users_bp, url_prefix="/admin/users")
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
        app.register_blueprint(documents_bp, url_prefix="/documents")
        logger.info("Documents blueprint registered")
    except Exception as e:
        logger.error(f"Error registering documents blueprint: {e}")
    
    try:
        # Register pdfs module
        from app.modules.pdfs.routes import pdfs_bp
        app.register_blueprint(pdfs_bp, url_prefix="/admin/pdfs")
        logger.info("PDFs blueprint registered")
    except Exception as e:
        logger.error(f"Error registering pdfs blueprint: {e}")
    
    try:
        # Register notifications module
        from app.modules.notifications.routes import notifications_bp
        app.register_blueprint(notifications_bp, url_prefix="/admin/notifications")
        logger.info("Notifications blueprint registered")
    except Exception as e:
        logger.error(f"Error registering notifications blueprint: {e}")
    
    try:
        # Register analytics module
        from app.modules.analytics.routes import analytics_bp
        app.register_blueprint(analytics_bp, url_prefix="/admin/analytics")
        logger.info("Analytics blueprint registered")
    except Exception as e:
        logger.error(f"Error registering analytics blueprint: {e}")
    
    try:
        # Register activity module
        from app.modules.activity.routes import activity_bp
        app.register_blueprint(activity_bp)
        logger.info("Activity blueprint registered")
    except Exception as e:
        logger.error(f"Error registering activity blueprint: {e}")
    
    try:
        # Register backup module
        from app.modules.backup.routes import backup_bp
        app.register_blueprint(backup_bp, url_prefix="/admin/backup")
        logger.info("Backup blueprint registered")
    except Exception as e:
        logger.error(f"Error registering backup blueprint: {e}")
    
    logger.info("All blueprints registered")


def register_user_loader(login_manager, db_manager):
    """Register user loader for Flask-Login"""
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.auth.models.user import User
        from app.modules.auth.repositories.user_repository import UserRepository
        
        user_repo = UserRepository(db_manager)
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


def initialize_default_data(db_manager):
    """Initialize default data for the application."""
    try:
        from app.modules.auth.repositories.user_repository import UserRepository
        user_repo = UserRepository(db_manager)
        user_repo.create_default_admin()
        logger.info("Default admin user created")
    except Exception as e:
        logger.error(f"Error creating default admin: {e}")


# Application instance for direct use
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
