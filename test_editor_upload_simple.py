#!/usr/bin/env python3
"""
Teste Simples do Sistema de Upload no Editor - Wiki Veloz Fibra
"""

import os
import time

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
EDITOR_UPLOAD_URL = f"{BASE_URL}/api/editor/upload"

def test_upload_system():
    """Testa o sistema de upload no editor"""
    print("🚀 TESTE SIMPLES DO UPLOAD NO EDITOR")
    print("=" * 50)
    
    # Criar sessão
    session = requests.Session()
    
    # 1. Fazer login
    print("📋 PASSO 1: Fazendo login...")
    login_data = {
        "username": "admin",
        "password": "Matheus Gallina"
    }
    
    try:
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        if response.status_code == 200:
            print("✅ Login realizado com sucesso")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    # 2. Criar arquivo de teste
    print("\n📋 PASSO 2: Criando arquivo de teste...")
    test_content = "Este é um arquivo de teste para o upload no editor."
    with open("test_upload.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    print("✅ Arquivo de teste criado")
    
    # 3. Testar upload
    print("\n📋 PASSO 3: Testando upload...")
    try:
        with open("test_upload.txt", "rb") as f:
            files = {"file": ("test_upload.txt", f, "text/plain")}
            response = session.post(EDITOR_UPLOAD_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload realizado com sucesso!")
            print(f"   📁 Arquivo: {result.get('filename')}")
            print(f"   🔗 URL: {result.get('url')}")
            print(f"   📏 Tamanho: {result.get('size')} bytes")
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
    
    # 4. Limpar arquivo de teste
    print("\n📋 PASSO 4: Limpando...")
    try:
        os.remove("test_upload.txt")
        print("✅ Arquivo de teste removido")
    except:
        pass
    
    print("\n🎉 TESTE CONCLUÍDO!")
    print("=" * 50)

if __name__ == "__main__":
    test_upload_system() 