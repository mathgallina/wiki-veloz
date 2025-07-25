"""
User repository for Wiki Veloz
CDD v2.0 - User data management
"""

import uuid
from datetime import datetime
from typing import List, Optional

from werkzeug.security import generate_password_hash

from app.core.database import DatabaseManager


class UserRepository:
    """Repository for user operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.filename = "users.json"
    
    def load_users(self) -> List[dict]:
        """Load all users"""
        return self.db_manager.load_data(self.filename)
    
    def save_users(self, users: List[dict]) -> bool:
        """Save all users"""
        return self.db_manager.save_data(self.filename, users)
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        return self.db_manager.get_by_id(self.filename, user_id)
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Get user by username"""
        users = self.load_users()
        return next((u for u in users if u.get('username') == username), None)
    
    def create_user(self, user_data: dict) -> bool:
        """Create new user"""
        users = self.load_users()
        
        # Generate ID if not provided
        if 'id' not in user_data:
            user_data['id'] = f"user-{uuid.uuid4().hex[:8]}"
        
        # Hash password if provided
        if 'password' in user_data:
            user_data['password_hash'] = generate_password_hash(
                user_data['password']
            )
            del user_data['password']
        
        # Add timestamps
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        
        users.append(user_data)
        return self.save_users(users)
    
    def update_user(self, user_id: str, updates: dict) -> bool:
        """Update user"""
        # Hash password if provided
        if 'password' in updates:
            updates['password_hash'] = generate_password_hash(
                updates['password']
            )
            del updates['password']
        
        updates['updated_at'] = datetime.now().isoformat()
        return self.db_manager.update_item(self.filename, user_id, updates)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        return self.db_manager.delete_item(self.filename, user_id)
    
    def create_default_admin(self) -> bool:
        """Create default admin user if none exists"""
        users = self.load_users()
        
        # Check if admin exists
        admin_exists = any(user.get('role') == 'admin' for user in users)
        
        if not admin_exists:
            admin_user = {
                'id': 'admin-001',
                'username': 'admin',
                'name': 'Matheus Gallina',
                'email': 'matheus@velozfibra.com',
                'password_hash': generate_password_hash('B@rcelona1998'),
                'role': 'admin',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'last_login': None,
                'is_active': True
            }
            users.append(admin_user)
            return self.save_users(users)
        
        return True
    
    def get_active_users(self) -> List[dict]:
        """Get all active users"""
        users = self.load_users()
        return [u for u in users if u.get('is_active', True)]
    
    def get_users_by_role(self, role: str) -> List[dict]:
        """Get users by role"""
        users = self.load_users()
        return [u for u in users if u.get('role') == role]
    
    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login time"""
        return self.update_user(user_id, {
            'last_login': datetime.now().isoformat()
        })
    
    def search_users(self, query: str) -> List[dict]:
        """Search users by name, username, or email"""
        users = self.load_users()
        query_lower = query.lower()
        
        results = []
        for user in users:
            if (query_lower in user.get('name', '').lower() or
                query_lower in user.get('username', '').lower() or
                query_lower in user.get('email', '').lower()):
                results.append(user)
        
        return results
