"""
Authentication routes for Wiki Veloz
CDD v2.0 - Authentication endpoints
"""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.core.config import config
from app.core.database import DatabaseManager
from app.modules.activity.decorators import log_user_action, log_user_management_action
from app.modules.auth.models.user import User
from app.modules.auth.services.auth_service import AuthService

# Initialize services
db_manager = DatabaseManager(config['default'])
auth_service = AuthService(db_manager)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_data = auth_service.authenticate_user(username, password)
        
        if user_data:
            user = User(
                user_data["id"],
                user_data["username"],
                user_data["name"],
                user_data["role"],
                user_data["created_at"],
            )
            login_user(user)
            
            flash(f'Bem-vindo, {user_data["name"]}!', "success")
            return redirect(url_for("main.index"))
        else:
            flash("Usuário ou senha incorretos.", "error")
    
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Logout user"""
    if current_user.is_authenticated:
        auth_service.log_activity(
            current_user.id,
            "logout",
            f"Logout realizado por {current_user.name}"
        )
    
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/admin/users")
@login_required
def admin_users():
    """Admin users page"""
    if not current_user.is_authenticated or current_user.role != "admin":
        flash(
            "Acesso negado. Apenas administradores podem acessar esta página.",
            "error",
        )
        return redirect(url_for("main.index"))
    
    users = auth_service.get_all_users()
    return render_template("admin_users.html", users=users)


@auth_bp.route("/api/users", methods=["GET"])
@login_required
def get_users():
    """Get all users (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    users = auth_service.get_active_users()
    return jsonify({"success": True, "data": users})


@auth_bp.route("/api/users", methods=["POST"])
@login_required
@log_user_management_action("user_create")
def create_user():
    """Create new user (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        user_data = request.get_json()
        
        # Validate user data
        is_valid, message = auth_service.validate_user_data(user_data)
        if not is_valid:
            return jsonify({"success": False, "message": message}), 400
        
        # Create user
        success = auth_service.create_user(user_data)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Usuário criado com sucesso"
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": "Erro ao criar usuário"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@auth_bp.route("/api/users/<user_id>", methods=["PUT"])
@login_required
@log_user_management_action("user_update")
def update_user(user_id):
    """Update user (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        updates = request.get_json()
        
        # Remove sensitive fields
        updates.pop('password_hash', None)
        updates.pop('created_at', None)
        
        success = auth_service.update_user(user_id, updates)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Usuário atualizado com sucesso"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@auth_bp.route("/api/users/<user_id>", methods=["DELETE"])
@login_required
@log_user_management_action("user_delete")
def delete_user(user_id):
    """Delete user (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        success = auth_service.delete_user(user_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Usuário deletado com sucesso"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@auth_bp.route("/api/users/search")
@login_required
def search_users():
    """Search users (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    query = request.args.get("q", "")
    if not query:
        return jsonify({"success": False, "message": "Query obrigatória"}), 400
    
    users = auth_service.search_users(query)
    return jsonify({"success": True, "data": users})


@auth_bp.route("/api/users/activities")
@login_required
def get_user_activities():
    """Get user activities (API)"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    activities = auth_service.get_user_activities()
    return jsonify({"success": True, "data": activities})


@auth_bp.route("/current-user", methods=["GET"])
@login_required
def get_current_user():
    """Get current user information"""
    try:
        user_data = {
            "id": current_user.id,
            "username": current_user.username,
            "name": current_user.name,
            "role": current_user.role,
            "created_at": current_user.created_at
        }
        
        return jsonify({
            "success": True,
            "data": user_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500
