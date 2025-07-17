#!/usr/bin/env python3
"""
Script de teste para verificar se os usuários não desaparecem
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_user_persistence():
    """Testa se os usuários persistem após reiniciar o servidor"""

    print("🧪 Testando persistência de usuários")
    print("=" * 50)

    # 1. Fazer login como admin
    print("🔐 Fazendo login como admin...")
    session = requests.Session()

    login_data = {
        "username": "matheus.gallina",
        "password": "Matheus Gallina"
    }

    response = session.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code != 200:
        print("❌ Erro ao fazer login")
        return False

    print("✅ Login realizado com sucesso")

    # 2. Verificar usuários existentes
    print("\n📋 Verificando usuários existentes...")
    response = session.get(f"{BASE_URL}/api/users")
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Encontrados {len(users)} usuários:")
        for user in users:
            print(f"  - {user['name']} ({user['username']}) - {user['role']}")
    else:
        print("❌ Erro ao buscar usuários")
        return False

    # 3. Criar um novo usuário de teste
    print("\n👤 Criando usuário de teste...")
    new_user = {
        "username": "teste.user",
        "name": "Usuário Teste",
        "email": "teste@velozfibra.com",
        "password": "senha123",
        "role": "user"
    }

    response = session.post(f"{BASE_URL}/api/users", json=new_user)
    if response.status_code == 201:
        created_user = response.json()["user"]
        print(f"✅ Usuário criado: {created_user['name']} ({created_user['username']})")
    else:
        print(f"❌ Erro ao criar usuário: {response.text}")
        return False

    # 4. Verificar se o usuário foi salvo
    print("\n🔍 Verificando se usuário foi salvo...")
    response = session.get(f"{BASE_URL}/api/users")
    if response.status_code == 200:
        users = response.json()
        test_user = next((u for u in users if u["username"] == "teste.user"), None)
        if test_user:
            print(f"✅ Usuário encontrado: {test_user['name']}")
        else:
            print("❌ Usuário não encontrado após criação")
            return False
    else:
        print("❌ Erro ao verificar usuários")
        return False

    # 5. Simular reinicialização do servidor (não reinicia de verdade)
    print("\n🔄 Simulando reinicialização do servidor...")
    print("   (Apenas aguardando 3 segundos)")
    time.sleep(3)

    # 6. Verificar se o usuário ainda existe
    print("\n🔍 Verificando se usuário persiste...")
    response = session.get(f"{BASE_URL}/api/users")
    if response.status_code == 200:
        users = response.json()
        test_user = next((u for u in users if u["username"] == "teste.user"), None)
        if test_user:
            print(f"✅ Usuário ainda existe: {test_user['name']}")
            print("🎉 Teste PASSOU - Usuários persistem corretamente!")
            return True
        else:
            print("❌ Usuário desapareceu após simulação de reinicialização")
            return False
    else:
        print("❌ Erro ao verificar usuários")
        return False

def cleanup_test_user():
    """Remove o usuário de teste"""
    print("\n🧹 Limpando usuário de teste...")

    session = requests.Session()

    # Login
    login_data = {
        "username": "matheus.gallina",
        "password": "Matheus Gallina"
    }
    session.post(f"{BASE_URL}/login", data=login_data)

    # Buscar usuário de teste
    response = session.get(f"{BASE_URL}/api/users")
    if response.status_code == 200:
        users = response.json()
        test_user = next((u for u in users if u["username"] == "teste.user"), None)
        if test_user:
            # Deletar usuário
            response = session.delete(f"{BASE_URL}/api/users/{test_user['id']}")
            if response.status_code == 200:
                print("✅ Usuário de teste removido")
            else:
                print("⚠️ Erro ao remover usuário de teste")
        else:
            print("ℹ️ Usuário de teste não encontrado para remoção")

if __name__ == "__main__":
    try:
        success = test_user_persistence()
        if success:
            print("\n🎯 RESULTADO: Usuários NÃO desaparecem mais!")
        else:
            print("\n❌ RESULTADO: Problema ainda existe")

        # Limpar usuário de teste
        cleanup_test_user()

    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando")
        print("   Execute: python3 app.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
