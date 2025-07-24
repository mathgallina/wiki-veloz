"""
User model for authentication
"""

from flask_login import UserMixin


class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, user_id, username, name, role, created_at):
        self.id = user_id
        self.username = username
        self.name = name
        self.role = role
        self.created_at = created_at

    def is_admin(self):
        """Check if user is admin"""
        return self.role == "admin"

    def is_authenticated(self):
        """Check if user is authenticated"""
        return True
