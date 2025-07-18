#!/usr/bin/env python3
"""
Script de teste para verificar o upload de arquivos
"""

import os
import tempfile

import requests


def test_upload():
    """Testa o upload de arquivos"""
    
    # URL do servidor
    base_url = "http://localhost:8000"
    
    # Fazer login primeiro
    login_data = {
        "username": "admin",
        "password": "B@rcelona1998"
    }
    
    session = requests.Session()
    
    # Fazer login
    print("🔐 Fazendo login...")
    login_response = session.post(f"{base_url}/login", data=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Erro no login: {login_response.status_code}")
        print(login_response.text)
        return
    
    print("✅ Login realizado com sucesso")
    
    # Criar arquivo de teste
    test_content = "Este é um arquivo de teste para upload."
    test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    test_file.write(test_content)
    test_file.close()
    
    print(f"📁 Arquivo de teste criado: {test_file.name}")
    
    # Testar upload
    print("📤 Testando upload...")
    
    with open(test_file.name, 'rb') as f:
        files = {'file': ('test_upload.txt', f, 'text/plain')}
        
        upload_response = session.post(
            f"{base_url}/api/editor/upload",
            files=files
        )
    
    # Limpar arquivo temporário
    os.unlink(test_file.name)
    
    print(f"📊 Status do upload: {upload_response.status_code}")
    print(f"📄 Resposta: {upload_response.text}")
    
    if upload_response.status_code == 200:
        print("✅ Upload realizado com sucesso!")
        result = upload_response.json()
        print(f"📋 Informações do arquivo:")
        print(f"   - Nome: {result.get('original_name')}")
        print(f"   - Tamanho: {result.get('size')} bytes")
        print(f"   - URL: {result.get('url')}")
    else:
        print("❌ Erro no upload")
        print(f"   - Status: {upload_response.status_code}")
        print(f"   - Resposta: {upload_response.text}")

if __name__ == "__main__":
    test_upload() 