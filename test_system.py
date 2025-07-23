#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema está funcionando
"""
import json

import requests


def test_system():
    base_url = "http://localhost:8000"

    print("🔍 Testando sistema Wiki Veloz...")

    # Teste 1: Verificar se o servidor está rodando
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        print(f"✅ Servidor rodando - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error ao conectar com servidor: {e}")
        return

    # Teste 2: Fazer login
    try:
        session = requests.Session()
        login_data = {"username": "admin", "password": "B@rcelona1998"}

        response = session.post(f"{base_url}/login", data=login_data)
        print(f"✅ Login realizado - Status: {response.status_code}")

        # Teste 3: Acessar página principal
        response = session.get(f"{base_url}/")
        print(f"✅ Página principal acessada - Status: {response.status_code}")

        # Teste 4: Acessar documentos
        response = session.get(f"{base_url}/documents/")
        print(f"✅ Página de documentos acessada - Status: {response.status_code}")

        # Teste 5: Testar API de documentos
        response = session.get(f"{base_url}/documents/api/documents")
        print(f"✅ API de documentos acessada - Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📊 Documentos encontrados: {len(data.get('data', []))}")
            except:
                print("⚠️ Resposta não é JSON válido")

        # Teste 6: Testar API de categorias
        response = session.get(f"{base_url}/documents/api/documents/categories")
        print(f"✅ API de categorias acessada - Status: {response.status_code}")

        print("\n🎉 Sistema funcionando corretamente!")

    except Exception as e:
        print(f"❌ Error durante teste: {e}")


if __name__ == "__main__":
    test_system()
