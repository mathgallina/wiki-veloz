#!/usr/bin/env python3
"""
Teste de Criação de Documentos
CDD v2.0 - Teste de funcionalidades de criação
"""

import json

import requests


def test_create_document():
    """Test document creation"""
    print("🔍 TESTANDO CRIAÇÃO DE DOCUMENTOS...")
    
    # Login first
    session = requests.Session()
    
    try:
        # Login
        login_data = {
            "username": "admin",
            "password": "B@rcelona1998"
        }
        
        response = session.post(
            "http://localhost:8000/auth/login",
            data=login_data,
            allow_redirects=True
        )
        
        if response.status_code == 200:
            print("✅ Login realizado com sucesso")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return
        
        # Test document creation
        document_data = {
            "title": "Documento de Teste via API",
            "content": "Este é um documento criado via API para testar o sistema.",
            "description": "Teste de criação via API com descrição válida",
            "type": "documento",
            "category": "Geral",
            "priority": "media",
            "author": "Matheus Gallina"
        }
        
        response = session.post(
            "http://localhost:8000/documents/create",
            json=document_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📄 Criação de documento: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Documento criado: {result.get('message', 'Sucesso')}")
            print(f"📋 ID do documento: {result.get('data', {}).get('id', 'N/A')}")
        else:
            print(f"❌ Erro na criação: {response.text}")
        
        # Test getting documents
        response = session.get("http://localhost:8000/documents/")
        
        if response.status_code == 200:
            documents = response.json()
            print(f"📚 Total de documentos: {documents.get('count', 0)}")
        else:
            print(f"❌ Erro ao listar documentos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_create_document() 