#!/usr/bin/env python3
"""
Debug do Sistema de Upload no Editor
"""

import json

import requests

BASE_URL = "http://localhost:8000"

def debug_upload():
    """Debug do sistema de upload"""
    session = requests.Session()
    
    # 1. Login
    print("🔐 Fazendo login...")
    login_data = {
        "username": "admin",
        "password": "Matheus Gallina"
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
    print(f"Status do login: {response.status_code}")
    print(f"URL final: {response.url}")
    
    # 2. Verificar se está logado
    print("\n🔍 Verificando se está logado...")
    response = session.get(f"{BASE_URL}/")
    print(f"Status da página principal: {response.status_code}")
    
    # 3. Testar upload com debug
    print("\n📤 Testando upload...")
    
    # Criar arquivo de teste
    with open("debug_test.txt", "w") as f:
        f.write("Teste de debug")
    
    try:
        with open("debug_test.txt", "rb") as f:
            files = {"file": ("debug_test.txt", f, "text/plain")}
            response = session.post(f"{BASE_URL}/api/editor/upload", files=files)
        
        print(f"Status do upload: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Conteúdo: {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"JSON: {json.dumps(result, indent=2)}")
            except:
                print("❌ Não foi possível parsear JSON")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
    
    # Limpar
    import os
    try:
        os.remove("debug_test.txt")
    except:
        pass

if __name__ == "__main__":
    debug_upload() 