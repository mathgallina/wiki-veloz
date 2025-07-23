"""
Wiki Veloz Fibra - Application Factory
=====================================

Factory pattern para inicialização da aplicação Flask de forma modular.
Permite configuração flexível e separação de responsabilidades.
"""

import logging
import os

from flask import Flask
from flask_login import LoginManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask.

    Args:
        config_name (str): Nome da configuração a set usada

    Returns:
        Flask: Instância da aplicação Flask configurada
    """
    app = Flask(__name__)

    # Configurações básicas
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # Configurar login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"

    # Registrar blueprints (serão adicionados conforme implementação)
    register_blueprints(app)

    # Registrar error handlers
    register_error_handlers(app)

    # Registrar context processors
    register_context_processors(app)

    logger.info("Aplicação Flask criada com sucesso")
    return app


def register_blueprints(app):
    """
    Registra todos os blueprints da aplicação.

    Args:
        app (Flask): Instância da aplicação Flask
    """
    # Registrar módulos usando factory pattern
    from app.modules.analytics import create_module as create_analytics_module
    from app.modules.backup import create_module as create_backup_module
    from app.modules.notifications import create_module as create_notifications_module
    from app.modules.pages import create_module as create_pages_module
    from app.modules.pdfs import create_module as create_pdfs_module
    from app.modules.users import create_module as create_users_module

    # Registrar todos os módulos
    create_users_module(app)
    create_pages_module(app)
    create_pdfs_module(app)
    create_notifications_module(app)
    create_analytics_module(app)
    create_backup_module(app)

    logger.info("Blueprints registrados")


def register_error_handlers(app):
    """
    Registra handlers de error personalizados.

    Args:
        app (Flask): Instância da aplicação Flask
    """

    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Página não encontrada"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Error interno do servidor"}, 500

    logger.info("Error handlers registrados")


def register_context_processors(app):
    """
    Registra context processors para variáveis globais.

    Args:
        app (Flask): Instância da aplicação Flask
    """

    @app.context_processor
    def inject_globals():
        return {"app_name": "Wiki Veloz Fibra", "app_version": "1.0.0"}

    logger.info("Context processors registrados")


# Instância da aplicação para uso direto
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
