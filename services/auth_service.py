"""
Authentication service for Wiki Veloz
CDD v2.0 - Authentication business logic
"""

from datetime import datetime
from typing import Optional

from werkzeug.security import check_password_hash

from app.core.database import ActivityLogger, DatabaseManager
from app.modules.auth.repositories.user_repository import UserRepository


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.user_repository = UserRepository(db_manager)
        self.activity_logger = ActivityLogger(db_manager)
    
    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with username and password"""
        user_data = self.user_repository.get_user_by_username(username)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            # Update last login
            self.user_repository.update_last_login(user_data['id'])
            
            # Log activity
            self.activity_logger.log_activity(
                user_data['id'],
                'login',
                f'Login realizado por {user_data["name"]}'
            )
            
            return user_data
        return None
    
    def create_default_admin(self) -> bool:
        """Create default admin user"""
        return self.user_repository.create_default_admin()
    
    def get_all_users(self) -> list:
        """Get all users"""
        return self.user_repository.load_users()
    
    def get_active_users(self) -> list:
        """Get active users"""
        return self.user_repository.get_active_users()
    
    def create_user(self, user_data: dict) -> bool:
        """Create new user"""
        success = self.user_repository.create_user(user_data)
        
        if success:
            self.activity_logger.log_activity(
                user_data.get('id', 'system'),
                'user_created',
                f'Usuário criado: {user_data.get("name", "Unknown")}'
            )
        
        return success
    
    def update_user(self, user_id: str, updates: dict) -> bool:
        """Update user"""
        success = self.user_repository.update_user(user_id, updates)
        
        if success:
            self.activity_logger.log_activity(
                user_id,
                'user_updated',
                f'Usuário atualizado: {updates.get("name", "Unknown")}'
            )
        
        return success
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user_data = self.user_repository.get_user_by_id(user_id)
        success = self.user_repository.delete_user(user_id)
        
        if success and user_data:
            self.activity_logger.log_activity(
                'system',
                'user_deleted',
                f'Usuário deletado: {user_data.get("name", "Unknown")}'
            )
        
        return success
    
    def search_users(self, query: str) -> list:
        """Search users"""
        return self.user_repository.search_users(query)
    
    def get_users_by_role(self, role: str) -> list:
        """Get users by role"""
        return self.user_repository.get_users_by_role(role)
    
    def log_activity(self, user_id: str, action: str, details: str = None) -> bool:
        """Log user activity"""
        return self.activity_logger.log_activity(user_id, action, details)
    
    def get_user_activities(self, user_id: str, limit: int = 50) -> list:
        """Get user activities"""
        return self.activity_logger.get_user_activities(user_id, limit)
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        return self.user_repository.get_user_by_id(user_id)
    
    def validate_user_data(self, user_data: dict) -> tuple[bool, str]:
        """Validate user data"""
        required_fields = ['username', 'name', 'email', 'role']
        
        for field in required_fields:
            if not user_data.get(field):
                return False, f'Campo obrigatório: {field}'
        
        # Check if username already exists
        existing_user = self.user_repository.get_user_by_username(
            user_data['username']
        )
        if existing_user:
            return False, 'Nome de usuário já existe'
        
        # Validate email format
        if '@' not in user_data['email']:
            return False, 'Email inválido'
        
        # Validate role
        valid_roles = ['admin', 'user']
        if user_data['role'] not in valid_roles:
            return False, 'Role inválido'
        
        return True, 'Dados válidos'
