"""
Authentication routes
"""

import json
import os
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.auth.models.user import User
from app.modules.auth.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Página de login"""
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

            # Atualizar último login
            auth_service.update_last_login(user_data["id"])

            # Registrar atividade
            auth_service.log_activity(
                user_data["id"],
                "login",
                f'Login realizado por {user_data["name"]}',
            )

            flash(f'Bem-vindo, {user_data["name"]}!', "success")
            return redirect(url_for("main.index"))
        else:
            flash("Usuário ou senha incorretos.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Logout do usuário"""
    if current_user.is_authenticated:
        auth_service.log_activity(
            current_user.id,
            "logout",
            f"Logout realizado por {current_user.name}",
        )
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/admin/users")
@login_required
def admin_users():
    """Página de administração de usuários (apenas para admins)"""
    if not current_user.is_authenticated or current_user.role != "admin":
        flash(
            "Acesso negado. Apenas administradores podem acessar esta página.",
            "error",
        )
        return redirect(url_for("main.index"))

    users = auth_service.get_all_users()
    return render_template("admin/users.html", users=users)
