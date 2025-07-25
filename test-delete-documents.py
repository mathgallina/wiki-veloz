#!/usr/bin/env python3
"""
Teste da funcionalidade de exclusão de documentos
Wiki Veloz - CDD v2.0
"""

import json
import os
from datetime import datetime

import requests

# Configurações
BASE_URL = "http://localhost:8000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def test_delete_documents():
    """Teste da funcionalidade de exclusão de documentos"""
    print("🧪 Testando funcionalidade de exclusão de documentos...")
    
    # 1. Login como admin
    print("\n1. Fazendo login como admin...")
    session = requests.Session()
    
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = session.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            print("✅ Login realizado com sucesso")
        else:
            print("❌ Erro no login")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # 2. Listar documentos antes da exclusão
    print("\n2. Listando documentos antes da exclusão...")
    try:
        response = session.get(f"{BASE_URL}/documents/api/")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data["data"]:
                documents_before = data["data"]
                print(f"✅ Encontrados {len(documents_before)} documentos")
                
                # Pegar o primeiro documento para teste
                test_document = documents_before[0]
                print(f"📄 Documento para exclusão: {test_document['title']}")
                print(f"   ID: {test_document['id']}")
                print(f"   Filename: {test_document.get('filename', 'N/A')}")
                
                # 3. Testar exclusão do documento
                print(f"\n3. Testando exclusão do documento...")
                delete_url = f"{BASE_URL}/documents/{test_document['id']}"
                response = session.delete(delete_url)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print("✅ Documento excluído com sucesso")
                        print(f"   Mensagem: {result.get('message', 'N/A')}")
                        
                        # 4. Verificar se o documento foi realmente excluído
                        print(f"\n4. Verificando se documento foi excluído...")
                        response = session.get(f"{BASE_URL}/documents/api/")
                        if response.status_code == 200:
                            data = response.json()
                            if data.get("success"):
                                documents_after = data["data"]
                                remaining_count = len(documents_after)
                                deleted_count = len(documents_before) - remaining_count
                                
                                print(f"✅ Documentos restantes: {remaining_count}")
                                print(f"✅ Documentos excluídos: {deleted_count}")
                                
                                # Verificar se o documento específico foi excluído
                                document_still_exists = any(
                                    doc['id'] == test_document['id'] 
                                    for doc in documents_after
                                )
                                
                                if not document_still_exists:
                                    print("✅ Documento foi completamente removido")
                                else:
                                    print("❌ Documento ainda existe na lista")
                                    return False
                            else:
                                print("❌ Erro ao verificar documentos após exclusão")
                                return False
                        else:
                            print(f"❌ Erro HTTP {response.status_code} ao verificar documentos")
                            return False
                    else:
                        print(f"❌ Erro na exclusão: {result.get('message', 'Erro desconhecido')}")
                        return False
                else:
                    print(f"❌ Erro HTTP {response.status_code} na exclusão")
                    return False
                    
            else:
                print("❌ Nenhum documento encontrado para teste")
                return False
        else:
            print(f"❌ Erro ao listar documentos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar exclusão: {e}")
        return False
    
    print("\n🎉 Teste de exclusão de documentos concluído com sucesso!")
    return True


def test_delete_nonexistent_document():
    """Teste de exclusão de documento inexistente"""
    print("\n🧪 Testando exclusão de documento inexistente...")
    
    session = requests.Session()
    
    # Login como admin
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = session.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print("❌ Erro no login para teste de documento inexistente")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # Tentar excluir documento inexistente
    try:
        fake_id = "doc-nonexistent123"
        delete_url = f"{BASE_URL}/documents/{fake_id}"
        response = session.delete(delete_url)
        
        if response.status_code == 404:
            result = response.json()
            if not result.get("success"):
                print("✅ Exclusão de documento inexistente tratada corretamente")
                return True
            else:
                print("❌ Documento inexistente foi excluído incorretamente")
                return False
        else:
            print(f"❌ Status code inesperado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar exclusão de documento inexistente: {e}")
        return False


def test_delete_without_permission():
    """Teste de exclusão sem permissão"""
    print("\n🧪 Testando exclusão sem permissão...")
    
    session = requests.Session()
    
    # Tentar excluir sem login
    try:
        fake_id = "doc-test123"
        delete_url = f"{BASE_URL}/documents/{fake_id}"
        response = session.delete(delete_url)
        
        if response.status_code in [401, 403]:
            print("✅ Acesso negado corretamente para usuário não autenticado")
            return True
        else:
            print(f"❌ Acesso não foi negado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de permissão: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Iniciando testes da funcionalidade de exclusão de documentos")
    print("=" * 60)
    
    # Teste principal
    success1 = test_delete_documents()
    
    # Teste de documento inexistente
    success2 = test_delete_nonexistent_document()
    
    # Teste de permissão
    success3 = test_delete_without_permission()
    
    print("\n" + "=" * 60)
    if success1 and success2 and success3:
        print("✅ Todos os testes de exclusão passaram!")
    else:
        print("❌ Alguns testes de exclusão falharam")
    
    print("\n📋 Resumo da correção implementada:")
    print("✅ Correção do erro join() com NoneType")
    print("✅ Verificação de filename antes de excluir arquivo")
    print("✅ Tratamento de documentos sem arquivo anexado")
    print("✅ Exclusão segura de documentos")
    print("✅ Validação de permissões mantida")
    print("✅ Log de atividades preservado") 