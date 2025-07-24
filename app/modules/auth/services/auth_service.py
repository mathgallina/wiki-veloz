"""
Authentication service
"""

import json
import os
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.auth.repositories.user_repository import UserRepository


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        users = self.user_repository.load_users()
        user_data = next((u for u in users if u["username"] == username), None)

        if user_data and check_password_hash(user_data["password_hash"], password):
            return user_data
        return None

    def create_default_admin(self):
        """Create default admin user"""
        users = self.user_repository.load_users()

        # Check if admin already exists
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
                "last_login": None,
            }
            users.append(admin_user)
            self.user_repository.save_users(users)

    def update_last_login(self, user_id):
        """Update user's last login time"""
        users = self.user_repository.load_users()
        for user in users:
            if user["id"] == user_id:
                user["last_login"] = datetime.now().isoformat()
                break
        self.user_repository.save_users(users)

    def get_all_users(self):
        """Get all users"""
        return self.user_repository.load_users()

    def log_activity(self, user_id, action, details=None):
        """Log user activity"""
        try:
            activity_log = []
            log_file = "app/data/activity_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    activity_log = json.load(f)

            activity = {
                "id": f"activity-{len(activity_log) + 1:06d}",
                "user_id": user_id,
                "action": action,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }

            activity_log.append(activity)

            # Keep only last 1000 activities
            if len(activity_log) > 1000:
                activity_log = activity_log[-1000:]

            os.makedirs("app/data", exist_ok=True)
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(activity_log, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Error logging activity: {e}")
