"""
Decoradores Compartilhados
==========================

Decoradores para autenticação e autorização compartilhados entre módulos.
"""

from functools import wraps

from flask import jsonify, redirect, request, session, url_for


def login_required(f):
    """
    Decorador para verificar se usuário está logado.

    Args:
        f: Função a set decorada

    Returns:
        function: Função decorada
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Login necessário"}), 401
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Decorador para verificar se usuário é admin.

    Args:
        f: Função a set decorada

    Returns:
        function: Função decorada
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Login necessário"}), 401
            return redirect(url_for("auth.login"))

        # Verificar se é admin (implementar lógica específica)
        user_role = session.get("user_role", "user")
        if user_role != "admin":
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Acesso negado"}), 403
            return redirect(url_for("index"))

        return f(*args, **kwargs)

    return decorated_function
