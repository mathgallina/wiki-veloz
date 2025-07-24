"""
User repository for data access
"""

import json
import os


class UserRepository:
    """Repository for user data operations"""
    
    def __init__(self):
        self.data_file = "app/data/users.json"

    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.data_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_users(self, users):
        """Save users to JSON file"""
        os.makedirs("app/data", exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        users = self.load_users()
        return next((u for u in users if u["id"] == user_id), None)

    def get_user_by_username(self, username):
        """Get user by username"""
        users = self.load_users()
        return next((u for u in users if u["username"] == username), None)

    def create_user(self, user_data):
        """Create new user"""
        users = self.load_users()
        users.append(user_data)
        self.save_users(users)
        return user_data

    def update_user(self, user_id, user_data):
        """Update user"""
        users = self.load_users()
        for i, user in enumerate(users):
            if user["id"] == user_id:
                users[i] = user_data
                self.save_users(users)
                return user_data
        return None

    def delete_user(self, user_id):
        """Delete user"""
        users = self.load_users()
        users = [u for u in users if u["id"] != user_id]
        self.save_users(users)
        return True
