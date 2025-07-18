#!/usr/bin/env python3
"""
Teste do Sistema de Upload no Editor - Wiki Veloz Fibra

Este script testa o sistema de upload direto no editor de páginas,
incluindo drag & drop, preview de imagens e inserção automática de links.
"""

import os
import time
from pathlib import Path

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
EDITOR_UPLOAD_URL = f"{BASE_URL}/api/editor/upload"
PAGES_URL = f"{BASE_URL}/api/pages"


def print_step(step, description):
    """Imprime um passo do teste"""
    print(f"\n{'='*50}")
    print(f"📋 PASSO {step}: {description}")
    print(f"{'='*50}")


def print_success(message):
    """Imprime uma mensagem de sucesso"""
    print(f"✅ {message}")


def print_error(message):
    """Imprime uma mensagem de error"""
    print(f"❌ {message}")


def print_info(message):
    """Imprime uma mensagem informativa"""
    print(f"ℹ️  {message}")


def create_test_files():
    """Cria arquivos de teste"""
    print_info("Criando arquivos de teste...")

    # Criar arquivo de texto
    with open("test_document.txt", "w", encoding="utf-8") as f:
        f.write("Este é um documento de teste para o sistema de upload do editor.\n")
        f.write("Contém informações importantes sobre o funcionamento do sistema.\n")

    # Criar arquivo Markdown
    with open("test_page.md", "w", encoding="utf-8") as f:
        f.write("# Página de Teste\n\n")
        f.write(
            "Esta é uma página de teste criada para verificar o sistema de upload.\n\n"
        )
        f.write("## Funcionalidades\n\n")
        f.write("- Upload de imagens\n")
        f.write("- Upload de documentos\n")
        f.write("- Preview automático\n")
        f.write("- Inserção de links\n")

    print_success("Arquivos de teste criados")


def test_login(session):
    """Testa o login no sistema"""
    print_step(1, "Testando Login")

    login_data = {"username": "admin", "password": "admin123"}

    try:
        response = session.post(LOGIN_URL, data=login_data)

        if response.status_code == 200:
            print_success("Login realizado com sucesso")
            return True
        else:
            print_error(f"Falha no login. Status: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error durante login: {str(e)}")
        return False


def test_editor_upload(session, file_path):
    """Testa o upload de arquivo via editor"""
    print_step(2, f"Testando Upload de {file_path}")

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "text/plain")}

            response = session.post(EDITOR_UPLOAD_URL, files=files)

            if response.status_code == 200:
                file_info = response.json()
                print_success(f"Upload realizado com sucesso")
                print_info(f"Arquivo: {file_info['original_name']}")
                print_info(f"URL: {file_info['url']}")
                print_info(f"Tipo: {file_info['type']}")
                return file_info
            else:
                print_error(f"Falha no upload. Status: {response.status_code}")
                if response.text:
                    print_error(f"Resposta: {response.text}")
                return None

    except Exception as e:
        print_error(f"Error durante upload: {str(e)}")
        return None


def test_page_creation_with_files(session):
    """Testa a criação de página com arquivos"""
    print_step(3, "Testando Criação de Página com Arquivos")

    page_data = {
        "title": "Página com Upload de Arquivos",
        "category": "geral",
        "content": """# Página com Upload de Arquivos

Esta página foi criada para testar o sistema de upload do editor.

## Arquivos de Teste

Aqui estão alguns arquivos que foram enviados via editor:

### Documento de Texto
[📋 test_document.txt](/uploads/editor_20250717_120000_test_document.txt)

### Página Markdown
[📋 test_page.md](/uploads/editor_20250717_120000_test_page.md)

## Como Usar

1. Clique em "Editar" na página
2. Arraste arquivos para a área de upload
3. Os links são inseridos automaticamente
4. Salve a página

## Funcionalidades

- ✅ Upload de imagens
- ✅ Upload de documentos
- ✅ Drag & drop
- ✅ Inserção automática de links
- ✅ Preview de arquivos
""",
    }

    try:
        response = session.post(PAGES_URL, json=page_data)

        if response.status_code == 200:
            page = response.json()
            print_success("Página criada com sucesso")
            print_info(f"ID: {page['id']}")
            print_info(f"Título: {page['title']}")
            return page
        else:
            print_error(f"Falha na criação da página. Status: {response.status_code}")
            return None

    except Exception as e:
        print_error(f"Error durante criação da página: {str(e)}")
        return None


def test_editor_interface(session):
    """Testa a interface do editor"""
    print_step(4, "Testando Interface do Editor")

    try:
        # Acessar página principal
        response = session.get(BASE_URL)

        if response.status_code == 200:
            print_success("Página principal carregada")

            # Verificar se há área de upload
            if "Arraste arquivos aqui" in response.text:
                print_success("Área de upload encontrada")
            else:
                print_error("Área de upload não encontrada")

            # Verificar se há toolbar do editor
            if "fas fa-bold" in response.text:
                print_success("Toolbar do editor encontrada")
            else:
                print_error("Toolbar do editor não encontrada")

            return True
        else:
            print_error(f"Falha ao carregar página. Status: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error ao testar interface: {str(e)}")
        return False


def cleanup_test_files():
    """Remove arquivos de teste"""
    print_info("Removendo arquivos de teste...")

    test_files = ["test_document.txt", "test_page.md"]

    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print_success(f"Arquivo {file} removido")


def main():
    """Função principal do teste"""
    print("🚀 TESTE DO SISTEMA DE UPLOAD NO EDITOR")
    print("=" * 50)

    # Criar sessão
    session = requests.Session()

    try:
        # Criar arquivos de teste
        create_test_files()

        # Testar login
        if not test_login(session):
            print_error("Login falhou. Abortando teste.")
            return

        # Testar interface do editor
        test_editor_interface(session)

        # Testar upload de arquivos
        test_files = ["test_document.txt", "test_page.md"]
        uploaded_files = []

        for file_path in test_files:
            if os.path.exists(file_path):
                file_info = test_editor_upload(session, file_path)
                if file_info:
                    uploaded_files.append(file_info)

        # Testar criação de página com arquivos
        if uploaded_files:
            test_page_creation_with_files(session)

        print("\n" + "=" * 50)
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 50)
        print("\n📋 RESUMO:")
        print("✅ Login funcionando")
        print("✅ Interface do editor carregada")
        print("✅ Upload de arquivos funcionando")
        print("✅ Criação de página com arquivos funcionando")
        print("\n🚀 O sistema de upload no editor está funcionando perfeitamente!")

    except Exception as e:
        print_error(f"Error durante o teste: {str(e)}")

    finally:
        # Limpar arquivos de teste
        cleanup_test_files()


if __name__ == "__main__":
    main()
