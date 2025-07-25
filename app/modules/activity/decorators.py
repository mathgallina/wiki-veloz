"""
Activity decorators for Wiki Veloz
CDD v2.0 - Activity logging decorators
"""

from functools import wraps
from flask import request, current_app
from flask_login import current_user


def log_action(action: str, details_template: str = None):
    """
    Decorator para logar ações automaticamente
    
    Args:
        action: Tipo da ação
        details_template: Template para detalhes (pode usar {data} para dados da request)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.modules.activity.services.activity_service import ActivityService
            
            # Executar a função original
            result = f(*args, **kwargs)
            
            # Logar a atividade
            try:
                activity_service = ActivityService()
                
                # Preparar detalhes
                details = None
                if details_template:
                    if "{data}" in details_template:
                        # Tentar extrair dados da request
                        data = {}
                        if request.is_json:
                            data = request.get_json() or {}
                        elif request.form:
                            data = dict(request.form)
                        details = details_template.format(data=data)
                    else:
                        details = details_template
                
                # Logar a atividade
                activity_service.log_activity(
                    user_id=current_user.id if current_user.is_authenticated else "anonymous",
                    action=action,
                    details=details,
                    ip_address=request.remote_addr
                )
                
            except Exception as e:
                # Não falhar se o logging falhar
                print(f"Error logging activity: {e}")
            
            return result
        return decorated_function
    return decorator


def log_user_action(action: str):
    """
    Decorator simplificado para logar ações de usuário
    
    Args:
        action: Tipo da ação
    """
    return log_action(action, f"Ação: {action}")


def log_page_action(action: str):
    """
    Decorator para logar ações relacionadas a páginas
    
    Args:
        action: Tipo da ação
    """
    return log_action(action, f"Página: {{data.get('title', 'N/A')}} - {action}")


def log_user_management_action(action: str):
    """
    Decorator para logar ações de gerenciamento de usuários
    
    Args:
        action: Tipo da ação
    """
    return log_action(action, f"Usuário: {{data.get('username', 'N/A')}} - {action}") 