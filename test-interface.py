#!/usr/bin/env python3
"""
Teste Rápido da Interface
"""

import time

import requests


def test_interface():
    """Test interface quickly"""
    print("🔍 TESTANDO INTERFACE...")
    
    # Test basic access
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Página principal: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na página principal: {e}")
        return
    
    # Test login page
    try:
        response = requests.get("http://localhost:8000/auth/login", timeout=5)
        print(f"✅ Página de login: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na página de login: {e}")
    
    # Test documents page (should redirect to login)
    try:
        response = requests.get("http://localhost:8000/documents", timeout=5)
        print(f"✅ Página de documentos: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na página de documentos: {e}")
    
    # Test pages page (should redirect to login)
    try:
        response = requests.get("http://localhost:8000/pages", timeout=5)
        print(f"✅ Página de páginas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na página de páginas: {e}")
    
    print("\n🌐 Para acessar a interface:")
    print("1. Abra: http://localhost:8000")
    print("2. Login: admin")
    print("3. Senha: B@rcelona1998")

if __name__ == "__main__":
    test_interface() 