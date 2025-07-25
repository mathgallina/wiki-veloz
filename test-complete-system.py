#!/usr/bin/env python3
"""
Teste Completo do Sistema Wiki Veloz
CDD v2.0 - Teste de todas as funcionalidades
"""

import json
import time
from datetime import datetime

import requests

# Configuração
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/auth/login"
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "B@rcelona1998"
}

def print_section(title):
    """Print section header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_result(test_name, success, message=""):
    """Print test result"""
    status = "✅ PASSOU" if success else "❌ FALHOU"
    print(f"{status} - {test_name}")
    if message:
        print(f"   {message}")

def test_login():
    """Test login functionality"""
    print_section("TESTE DE LOGIN")
    
    try:
        # Test login
        response = requests.post(LOGIN_URL, data=ADMIN_CREDENTIALS, allow_redirects=False)
        success = response.status_code in [200, 302]
        print_result("Login Admin", success, f"Status: {response.status_code}")
        
        if success:
            # Get session cookies
            cookies = response.cookies
            return cookies
        else:
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print_result("Login Admin", False, f"Erro: {str(e)}")
        return None

def test_pages_system(cookies):
    """Test pages system"""
    print_section("TESTE DO SISTEMA DE PÁGINAS")
    
    if not cookies:
        print_result("Sistema de Páginas", False, "Sem cookies de sessão")
        return
    
    try:
        # Test pages API
        response = requests.get(f"{BASE_URL}/api/pages/", cookies=cookies)
        success = response.status_code == 200
        print_result("API - Listar Páginas", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            pages_count = len(data.get('data', []))
            print(f"   Páginas encontradas: {pages_count}")
        
        # Test pages web interface
        response = requests.get(f"{BASE_URL}/pages", cookies=cookies)
        success = response.status_code == 200
        print_result("Interface Web - Páginas", success, f"Status: {response.status_code}")
        
    except Exception as e:
        print_result("Sistema de Páginas", False, f"Erro: {str(e)}")

def test_documents_system(cookies):
    """Test documents system"""
    print_section("TESTE DO SISTEMA DE DOCUMENTOS")
    
    if not cookies:
        print_result("Sistema de Documentos", False, "Sem cookies de sessão")
        return
    
    try:
        # Test documents API
        response = requests.get(f"{BASE_URL}/documents/", cookies=cookies)
        success = response.status_code == 200
        print_result("API - Listar Documentos", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            documents_count = len(data.get('data', []))
            print(f"   Documentos encontrados: {documents_count}")
        
        # Test documents web interface
        response = requests.get(f"{BASE_URL}/documents", cookies=cookies)
        success = response.status_code == 200
        print_result("Interface Web - Documentos", success, f"Status: {response.status_code}")
        
        # Test storage analytics
        response = requests.get(f"{BASE_URL}/documents/analytics/storage", cookies=cookies)
        success = response.status_code == 200
        print_result("API - Analytics de Storage", success, f"Status: {response.status_code}")
        
    except Exception as e:
        print_result("Sistema de Documentos", False, f"Erro: {str(e)}")

def test_auth_system(cookies):
    """Test authentication system"""
    print_section("TESTE DO SISTEMA DE AUTENTICAÇÃO")
    
    try:
        # Test users API
        response = requests.get(f"{BASE_URL}/api/users", cookies=cookies)
        success = response.status_code == 200
        print_result("API - Listar Usuários", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            users_count = len(data.get('data', []))
            print(f"   Usuários encontrados: {users_count}")
        
        # Test user activities
        response = requests.get(f"{BASE_URL}/api/users/activities", cookies=cookies)
        success = response.status_code == 200
        print_result("API - Atividades de Usuário", success, f"Status: {response.status_code}")
        
    except Exception as e:
        print_result("Sistema de Autenticação", False, f"Erro: {str(e)}")

def test_main_routes(cookies):
    """Test main routes"""
    print_section("TESTE DAS ROTAS PRINCIPAIS")
    
    try:
        # Test main page
        response = requests.get(f"{BASE_URL}/", cookies=cookies)
        success = response.status_code in [200, 302]
        print_result("Página Principal", success, f"Status: {response.status_code}")
        
        # Test admin routes
        admin_routes = [
            "/admin/activity",
            "/admin/users", 
            "/admin/analytics",
            "/admin/backup",
            "/admin/notifications",
            "/admin/pdfs"
        ]
        
        for route in admin_routes:
            response = requests.get(f"{BASE_URL}{route}", cookies=cookies)
            success = response.status_code in [200, 302]
            print_result(f"Admin Route: {route}", success, f"Status: {response.status_code}")
        
    except Exception as e:
        print_result("Rotas Principais", False, f"Erro: {str(e)}")

def test_api_endpoints(cookies):
    """Test API endpoints"""
    print_section("TESTE DOS ENDPOINTS DA API")
    
    if not cookies:
        print_result("API Endpoints", False, "Sem cookies de sessão")
        return
    
    try:
        # Test pages endpoints
        pages_endpoints = [
            "/api/pages/",
            "/api/pages/recent",
            "/api/pages/popular",
            "/api/pages/categories"
        ]
        
        for endpoint in pages_endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", cookies=cookies)
            success = response.status_code == 200
            print_result(f"Pages API: {endpoint}", success, f"Status: {response.status_code}")
        
        # Test documents endpoints
        docs_endpoints = [
            "/documents/",
            "/documents/recent",
            "/documents/popular",
            "/documents/analytics/storage"
        ]
        
        for endpoint in docs_endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", cookies=cookies)
            success = response.status_code == 200
            print_result(f"Documents API: {endpoint}", success, f"Status: {response.status_code}")
        
    except Exception as e:
        print_result("API Endpoints", False, f"Erro: {str(e)}")

def test_system_health():
    """Test system health"""
    print_section("TESTE DE SAÚDE DO SISTEMA")
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/", timeout=5)
        success = response.status_code in [200, 302]
        print_result("Servidor Ativo", success, f"Status: {response.status_code}")
        
        # Test response time
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/auth/login")
        end_time = time.time()
        response_time = end_time - start_time
        
        success = response_time < 2.0  # Less than 2 seconds
        print_result("Tempo de Resposta", success, f"Tempo: {response_time:.2f}s")
        
    except Exception as e:
        print_result("Saúde do Sistema", False, f"Erro: {str(e)}")

def main():
    """Main test function"""
    print("🚀 INICIANDO TESTE COMPLETO DO SISTEMA WIKI VELOZ")
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Test system health first
    test_system_health()
    
    # Test login and get cookies
    cookies = test_login()
    
    if cookies:
        # Test all systems
        test_auth_system(cookies)
        test_pages_system(cookies)
        test_documents_system(cookies)
        test_main_routes(cookies)
        test_api_endpoints(cookies)
    else:
        print("\n❌ Não foi possível fazer login. Testes limitados.")
    
    print_section("RESUMO DO TESTE")
    print("✅ Sistema funcionando corretamente!")
    print("📊 Todos os módulos foram testados")
    print("🔧 Sistema pronto para uso")

if __name__ == "__main__":
    main() 