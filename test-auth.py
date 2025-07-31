#!/usr/bin/env python3
"""
Teste de Autenticação
CDD v2.0 - Teste de login
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import DatabaseManager
from app.core.config import config
from app.modules.auth.services.auth_service import AuthService


def test_auth():
    """Test authentication"""
    print("🔐 TESTE DE AUTENTICAÇÃO")
    
    # Initialize services
    db_manager = DatabaseManager(config['default']())
    auth_service = AuthService(db_manager)
    
    # Test credentials
    credentials = [
        ("admin", "B@rcelona1998"),
        ("admin", "admin123"),
        ("admin", "admin"),
        ("bruna", "bruna123"),
        ("bruna", "bruna")
    ]
    
    for username, password in credentials:
        print(f"\nTestando: {username} / {password}")
        
        # Test authentication
        user = auth_service.authenticate_user(username, password)
        
        if user:
            print(f"✅ Login bem-sucedido para {username}")
            print(f"   Nome: {user['name']}")
            print(f"   Role: {user['role']}")
            print(f"   Ativo: {user['is_active']}")
        else:
            print(f"❌ Login falhou para {username}")
    
    # Test user creation
    print(f"\n🔧 TESTE DE CRIAÇÃO DE USUÁRIO")
    
    test_user_data = {
        "username": "teste",
        "name": "Usuário Teste",
        "email": "teste@velozfibra.com",
        "password": "teste123",
        "role": "user"
    }
    
    success = auth_service.create_user(test_user_data)
    print(f"Criação de usuário: {'✅' if success else '❌'}")
    
    # Test login with new user
    if success:
        user = auth_service.authenticate_user("teste", "teste123")
        if user:
            print(f"✅ Login com novo usuário bem-sucedido")
        else:
            print(f"❌ Login com novo usuário falhou")


if __name__ == "__main__":
    test_auth() 