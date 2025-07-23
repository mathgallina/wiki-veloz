#!/usr/bin/env python3
"""
Script para testar o deploy no Render
"""

import requests
import time

def test_deploy():
    url = "https://wiki-veloz.onrender.com"
    
    print("🧪 Testando deploy no Render...")
    print(f"URL: {url}")
    
    try:
        # Testar endpoint raiz
        print("\n1. Testando endpoint raiz...")
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        # Testar endpoint de debug
        print("\n2. Testando endpoint de debug...")
        response = requests.get(f"{url}/debug", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Testar endpoint de login
        print("\n3. Testando endpoint de login...")
        response = requests.get(f"{url}/login", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        print("\n✅ Testes concluídos!")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - Servidor pode estar iniciando")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Servidor pode estar offline")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_deploy()
