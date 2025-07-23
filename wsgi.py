import os
import json
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "veloz-fibra-secret-key-2024")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login to access this page."

# User class
class User(UserMixin):
    def __init__(self, user_id, username, name, role, created_at):
        self.id = user_id
        self.username = username
        self.name = name
        self.role = role
        self.created_at = created_at

# Functions to manage users
def load_users():
    try:
        with open("data/users.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

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
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        users.append(admin_user)
        save_users(users)
        print("✅ Admin user created")

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    user_data = next((u for u in users if u["id"] == user_id), None)
    if user_data and user_data.get("is_active", True):
        return User(
            user_data["id"],
            user_data["username"],
            user_data["name"],
            user_data["role"],
            user_data["created_at"]
        )
    return None

@app.route("/")
@login_required
def index():
    """Main page (protected)"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
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
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for("login"))

@app.route("/documents/")
@login_required
def documents():
    """Documents page"""
    return render_template("documents/index.html")

@app.route("/debug")
def debug():
    """Debug endpoint to check if app is running"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.9+",
        "environment": os.environ.get("FLASK_ENV", "production"),
        "port": os.environ.get("PORT", "10000")
    })

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route("/api/test")
def api_test():
    """API test endpoint"""
    return jsonify({
        "message": "API working",
        "status": "ok"
    })

if __name__ == "__main__":
    create_default_admin()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
