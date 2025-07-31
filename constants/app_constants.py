"""
Wiki Veloz Fibra - Constantes da Aplicação
CDD v2.0 - Centralização de constantes e configurações
"""

# Configurações da Aplicação
APP_NAME = "Wiki Veloz Fibra"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Wiki Interna da Veloz Fibra"

# Configurações de Upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Configurações de Paginação
ITEMS_PER_PAGE = 10
MAX_ITEMS_PER_PAGE = 100

# Configurações de Sessão
SESSION_TIMEOUT = 3600  # 1 hora
REMEMBER_COOKIE_DURATION = 30 * 24 * 3600  # 30 dias

# Configurações de Backup
BACKUP_RETENTION_DAYS = 30
BACKUP_MAX_SIZE = 100 * 1024 * 1024  # 100MB

# Configurações de Notificações
NOTIFICATION_RETENTION_DAYS = 30
MAX_NOTIFICATIONS_PER_USER = 100

# Cores do Sistema (Tailwind CSS)
COLORS = {
    'primary': '#3B82F6',      # blue-500
    'secondary': '#6B7280',    # gray-500
    'success': '#10B981',      # emerald-500
    'warning': '#F59E0B',      # amber-500
    'danger': '#EF4444',       # red-500
    'info': '#06B6D4',         # cyan-500
    'light': '#F9FAFB',        # gray-50
    'dark': '#111827',         # gray-900
}

# Ícones do Sistema (Heroicons)
ICONS = {
    'home': 'home',
    'user': 'user',
    'document': 'document',
    'folder': 'folder',
    'upload': 'upload',
    'download': 'download',
    'edit': 'pencil',
    'delete': 'trash',
    'search': 'magnifying-glass',
    'settings': 'cog',
    'backup': 'cloud-arrow-up',
    'notification': 'bell',
    'analytics': 'chart-bar',
    'admin': 'shield-check',
    'logout': 'arrow-right-on-rectangle',
}

# Mensagens do Sistema
MESSAGES = {
    'login_success': 'Login realizado com sucesso!',
    'login_error': 'Usuário ou senha incorretos.',
    'logout_success': 'Logout realizado com sucesso!',
    'document_created': 'Documento criado com sucesso!',
    'document_updated': 'Documento atualizado com sucesso!',
    'document_deleted': 'Documento excluído com sucesso!',
    'upload_success': 'Arquivo enviado com sucesso!',
    'upload_error': 'Erro ao enviar arquivo.',
    'backup_created': 'Backup criado com sucesso!',
    'backup_restored': 'Backup restaurado com sucesso!',
    'notification_sent': 'Notificação enviada com sucesso!',
    'permission_denied': 'Acesso negado. Permissão insuficiente.',
    'page_not_found': 'Página não encontrada.',
    'server_error': 'Erro interno do servidor.',
}

# Status de Documentos
DOCUMENT_STATUS = {
    'draft': 'rascunho',
    'published': 'publicado',
    'archived': 'arquivado',
    'deleted': 'excluído',
}

# Tipos de Usuário
USER_ROLES = {
    'admin': 'Administrador',
    'user': 'Usuário',
    'editor': 'Editor',
    'viewer': 'Visualizador',
}

# Tipos de Notificação
NOTIFICATION_TYPES = {
    'system': 'Sistema',
    'user': 'Usuário',
    'document': 'Documento',
    'backup': 'Backup',
    'security': 'Segurança',
}

# Configurações de API
API_ENDPOINTS = {
    'auth': '/api/auth',
    'users': '/api/users',
    'documents': '/api/documents',
    'pages': '/api/pages',
    'backup': '/api/backup',
    'analytics': '/api/analytics',
    'notifications': '/api/notifications',
}

# Configurações de Segurança
SECURITY_CONFIG = {
    'password_min_length': 8,
    'password_require_special': True,
    'password_require_numbers': True,
    'password_require_uppercase': True,
    'max_login_attempts': 5,
    'lockout_duration': 300,  # 5 minutos
}

# Configurações de Log
LOG_LEVELS = {
    'debug': 'DEBUG',
    'info': 'INFO',
    'warning': 'WARNING',
    'error': 'ERROR',
    'critical': 'CRITICAL',
}

# Configurações de Cache
CACHE_CONFIG = {
    'default_timeout': 300,  # 5 minutos
    'max_size': 1000,
    'cleanup_interval': 600,  # 10 minutos
}

# Configurações de Email
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'max_retries': 3,
}

# Configurações do Google Drive
GOOGLE_DRIVE_CONFIG = {
    'scopes': ['https://www.googleapis.com/auth/drive.file'],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_folder_name': 'Wiki Veloz Backups',
    'sync_interval': 3600,  # 1 hora
}

# Configurações de Analytics
ANALYTICS_CONFIG = {
    'track_page_views': True,
    'track_user_actions': True,
    'track_document_views': True,
    'retention_days': 90,
    'privacy_compliant': True,
} 