"""
Configurações da Aplicação
=========================

Configurações centralizadas para diferentes ambientes.
"""

import os


class Config:
    """Configuração base para todos os ambientes."""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-in-production'
    )
    DEBUG = False
    TESTING = False
    
    # Configurações de dados
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    PAGES_FILE = os.path.join(DATA_DIR, 'pages.json')
    PDFS_FILE = os.path.join(DATA_DIR, 'pdfs.json')
    NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')
    ACTIVITY_LOG_FILE = os.path.join(DATA_DIR, 'activity_log.json')
    
    # Configurações de upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Configurações de sessão
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configurações de backup
    BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
    BACKUP_RETENTION_DAYS = 30
    
    # Configurações do Google Drive (opcional)
    GOOGLE_DRIVE_CREDENTIALS_FILE = os.environ.get(
        'GOOGLE_DRIVE_CREDENTIALS_FILE'
    )
    GOOGLE_DRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    
    # Configurações de email (opcional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação."""
        pass


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento."""
    
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações de desenvolvimento."""
        import logging
        logging.basicConfig(level=logging.DEBUG)


class TestingConfig(Config):
    """Configuração para testes."""
    
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    
    # Usar diretórios temporários para testes
    DATA_DIR = '/tmp/wiki_veloz_test_data'
    UPLOAD_FOLDER = '/tmp/wiki_veloz_test_uploads'
    BACKUP_DIR = '/tmp/wiki_veloz_test_backups'


class ProductionConfig(Config):
    """Configuração para produção."""
    
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações de produção."""
        import logging
        from logging.handlers import RotatingFileHandler

        # Configurar logging para arquivo
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/wiki_veloz.log', maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Wiki Veloz startup')


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:  # type: ignore
    """
    Retorna a configuração apropriada.
    
    Args:
        config_name (str): Nome da configuração
        
    Returns:
        Config: Classe de configuração
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    return config.get(config_name, config['default']) 