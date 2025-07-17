#!/usr/bin/env python3
"""
Script de teste para o sistema de PDFs da Wiki Veloz Fibra
"""

import os
import json
import requests
from pathlib import Path

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
PDFS_URL = f"{BASE_URL}/api/pdfs"
UPLOAD_URL = f"{BASE_URL}/api/pdfs"

# Credenciais de teste
LOGIN_DATA = {
    "username": "matheus.gallina",
    "password": "B@rcelona1998"
}

def test_login():
    """Testa o login e retorna a sessão"""
    print("🔐 Testando login...")

    session = requests.Session()

    # Fazer login
    response = session.post(LOGIN_URL, data=LOGIN_DATA, allow_redirects=True)

    if response.status_code == 200:
        print("✅ Login realizado com sucesso")
        return session
    else:
        print(f"❌ Erro no login: {response.status_code}")
        return None

def test_get_pdfs(session):
    """Testa a listagem de PDFs"""
    print("\n📄 Testando listagem de PDFs...")

    response = session.get(PDFS_URL)

    if response.status_code == 200:
        data = response.json()
        pdfs = data.get("pdfs", [])
        print(f"✅ Encontrados {len(pdfs)} PDFs")

        for pdf in pdfs:
            print(f"  - {pdf['original_filename']} ({pdf['file_size']} bytes)")

        return pdfs
    else:
        print(f"❌ Erro ao listar PDFs: {response.status_code}")
        return []

def test_upload_pdf(session, file_path):
    """Testa o upload de um PDF"""
    print(f"\n📤 Testando upload de {file_path}...")

    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return None

    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'page_id': '',  # Sem associação
            'description': 'Teste de upload via script'
        }

        response = session.post(UPLOAD_URL, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload realizado com sucesso")
        print(f"  - ID: {result['pdf']['id']}")
        print(f"  - Nome: {result['pdf']['original_filename']}")
        print(f"  - Tamanho: {result['pdf']['file_size']} bytes")
        return result['pdf']
    else:
        print(f"❌ Erro no upload: {response.status_code}")
        print(f"  Resposta: {response.text}")
        return None

def test_download_pdf(session, pdf):
    """Testa o download de um PDF"""
    print(f"\n⬇️ Testando download de {pdf['original_filename']}...")

    download_url = f"{BASE_URL}/uploads/{pdf['filename']}"
    response = session.get(download_url)

    if response.status_code == 200:
        print(f"✅ Download realizado com sucesso")
        print(f"  - Tamanho baixado: {len(response.content)} bytes")

        # Salvar arquivo de teste
        test_file = f"test_download_{pdf['original_filename']}"
        with open(test_file, 'wb') as f:
            f.write(response.content)
        print(f"  - Arquivo salvo como: {test_file}")

        return True
    else:
        print(f"❌ Erro no download: {response.status_code}")
        return False

def test_view_pdf(session, pdf):
    """Testa a visualização de um PDF"""
    print(f"\n👁️ Testando visualização de {pdf['original_filename']}...")

    view_url = f"{BASE_URL}/api/pdfs/{pdf['id']}/view"
    response = session.get(view_url)

    if response.status_code == 200:
        print(f"✅ Visualização disponível")
        print(f"  - Content-Type: {response.headers.get('content-type')}")
        print(f"  - Tamanho: {len(response.content)} bytes")
        return True
    else:
        print(f"❌ Erro na visualização: {response.status_code}")
        return False

def test_delete_pdf(session, pdf):
    """Testa a exclusão de um PDF"""
    print(f"\n🗑️ Testando exclusão de {pdf['original_filename']}...")

    delete_url = f"{BASE_URL}/api/pdfs/{pdf['id']}"
    response = session.delete(delete_url)

    if response.status_code == 200:
        print(f"✅ PDF excluído com sucesso")
        return True
    else:
        print(f"❌ Erro na exclusão: {response.status_code}")
        print(f"  Resposta: {response.text}")
        return False

def create_test_pdf():
    """Cria um PDF de teste"""
    print("\n📝 Criando PDF de teste...")

    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        test_file = "test_document.pdf"
        c = canvas.Canvas(test_file, pagesize=letter)

        # Adicionar conteúdo
        c.drawString(100, 750, "Teste do Sistema de PDFs")
        c.drawString(100, 720, "Wiki Veloz Fibra")
        c.drawString(100, 690, "Este é um documento de teste para verificar")
        c.drawString(100, 660, "o funcionamento do sistema de upload de PDFs.")

        c.drawString(100, 600, "Funcionalidades testadas:")
        c.drawString(120, 570, "• Upload de arquivos")
        c.drawString(120, 540, "• Visualização no navegador")
        c.drawString(120, 510, "• Download de arquivos")
        c.drawString(120, 480, "• Exclusão de arquivos")

        c.drawString(100, 400, "Data: 16/07/2025")
        c.drawString(100, 370, "Sistema: Wiki Veloz Fibra")

        c.save()
        print(f"✅ PDF de teste criado: {test_file}")
        return test_file

    except ImportError:
        print("⚠️ reportlab não disponível, criando arquivo de texto...")

        test_file = "test_document.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Teste do Sistema de PDFs\n")
            f.write("Wiki Veloz Fibra\n\n")
            f.write("Este é um documento de teste para verificar\n")
            f.write("o funcionamento do sistema de upload de arquivos.\n\n")
            f.write("Funcionalidades testadas:\n")
            f.write("• Upload de arquivos\n")
            f.write("• Visualização no navegador\n")
            f.write("• Download de arquivos\n")
            f.write("• Exclusão de arquivos\n\n")
            f.write("Data: 16/07/2025\n")
            f.write("Sistema: Wiki Veloz Fibra\n")

        print(f"✅ Arquivo de teste criado: {test_file}")
        return test_file

def check_server_status():
    """Verifica se o servidor está rodando"""
    print("🔍 Verificando status do servidor...")

    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando")
            return True
        else:
            print(f"⚠️ Servidor respondeu com status {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando")
        print("  Execute: python3 app.py")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do sistema de PDFs")
    print("=" * 50)

    # Verificar servidor
    if not check_server_status():
        return

    # Fazer login
    session = test_login()
    if not session:
        return

    # Listar PDFs existentes
    existing_pdfs = test_get_pdfs(session)

    # Criar arquivo de teste
    test_file = create_test_pdf()

    # Testar upload
    uploaded_pdf = test_upload_pdf(session, test_file)
    if not uploaded_pdf:
        return

    # Testar download
    test_download_pdf(session, uploaded_pdf)

    # Testar visualização
    test_view_pdf(session, uploaded_pdf)

    # Listar PDFs novamente
    print("\n📄 Listando PDFs após upload...")
    test_get_pdfs(session)

    # Testar exclusão (apenas se for admin)
    if input("\n🗑️ Deseja testar a exclusão? (s/n): ").lower() == 's':
        test_delete_pdf(session, uploaded_pdf)

    # Limpar arquivo de teste
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🧹 Arquivo de teste removido: {test_file}")

    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main()
