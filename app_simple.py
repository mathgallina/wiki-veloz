import json
import os
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça login para acessar esta página."

# Classe de usuário
class User(UserMixin):
    def __init__(self, user_id, username, name, role, created_at):
        self.id = user_id
        self.username = username
        self.name = name
        self.role = role
        self.created_at = created_at

# Funções para gerenciar usuários
def load_users():
    try:
        with open("data/users.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def create_default_admin():
    users = load_users()
    admin_exists = any(user["role"] == "admin" for user in users)
    
    if not admin_exists:
        admin_user = {
            "id": "admin-001",
            "username": "admin",
            "name": "Matheus Gallina",
            "email": "matheus@velozfibra.com",
            "password_hash": generate_password_hash("B@rcelona1998"),
            "role": "admin",
            "created_at": datetime.now().isoformat()
        }
        users.append(admin_user)
        
        os.makedirs("data", exist_ok=True)
        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return User(
                user["id"],
                user["username"],
                user["name"],
                user["role"],
                user["created_at"]
            )
    return None

@app.route("/debug")
def debug():
    """Endpoint de debug para verificar se o app está rodando"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.9+",
        "environment": os.environ.get("FLASK_ENV", "production")
    })

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        users = load_users()
        user_data = next((u for u in users if u["username"] == username), None)
        
        if user_data and check_password_hash(user_data["password_hash"], password):
            user = User(
                user_data["id"],
                user_data["username"],
                user_data["name"],
                user_data["role"],
                user_data["created_at"]
            )
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciais inválidas")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/documents/")
@login_required
def documents():
    return render_template("documents/index.html")

if __name__ == "__main__":
    create_default_admin()
    app.run(debug=True, host="0.0.0.0", port=8000)
