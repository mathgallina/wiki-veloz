"""
Custom decorators for Wiki Veloz
"""

from functools import wraps
from flask import jsonify, flash, redirect, url_for
from flask_login import current_user, login_required


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        
        if current_user.role != "admin":
            flash("Acesso negado. Apenas administradores podem acessar esta página.", "error")
            return redirect(url_for("main.index"))
        
        return f(*args, **kwargs)
    return decorated_function


def api_response(success=True, data=None, message=None, status_code=200):
    """Decorator to standardize API responses"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return jsonify({
                    "success": success,
                    "data": result if data is None else data,
                    "message": message
                }), status_code
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "message": "Internal server error"
                }), 500
        return decorated_function
    return decorator


def validate_json(*required_fields):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Invalid JSON data"}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def log_activity(action):
    """Decorator to log user activity"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.modules.auth.services.auth_service import AuthService
            
            result = f(*args, **kwargs)
            
            if current_user.is_authenticated:
                auth_service = AuthService()
                auth_service.log_activity(
                    current_user.id,
                    action,
                    f"Function {f.__name__} executed"
                )
            
            return result
        return decorated_function
    return decorator


def handle_errors(f):
    """Decorator to handle common errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FileNotFoundError:
            return jsonify({"error": "Resource not found"}), 404
        except PermissionError:
            return jsonify({"error": "Permission denied"}), 403
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
    return decorated_function
