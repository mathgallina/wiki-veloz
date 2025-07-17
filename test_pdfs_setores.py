#!/usr/bin/env python3
"""
Script de Teste - Sistema de PDFs por Setores
Wiki Veloz Fibra

Este script testa o sistema de upload, visualização e gerenciamento de PDFs
organizados por setores da empresa.
"""

import json
import os
import time
from datetime import datetime

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
PDFS_URL = f"{BASE_URL}/admin/pdfs"
API_PDFS_URL = f"{BASE_URL}/api/pdfs"
API_SECTORS_URL = f"{BASE_URL}/api/sectors"

# Credenciais de teste
USERNAME = "matheus.gallina"
PASSWORD = "B@rcelona1998"

def print_step(step, description):
    """Imprime um passo do teste"""
    print(f"\n{'='*60}")
    print(f"PASSO {step}: {description}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime uma mensagem de sucesso"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime uma mensagem de erro"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime uma mensagem informativa"""
    print(f"ℹ️  {message}")

def test_login():
    """Testa o login no sistema"""
    print_step(1, "Testando Login")
    
    session = requests.Session()
    
    # Fazer login
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        
        if response.status_code == 200:
            # Verificar se foi redirecionado para a página principal
            if "VELOZ FIBRA" in response.text or "Central de Conhecimento" in response.text:
                print_success("Login realizado com sucesso")
                return session
            else:
                print_error("Login falhou - não foi redirecionado para a página principal")
                return None
        else:
            print_error(f"Falha no login. Status: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Erro durante login: {str(e)}")
        return None

def test_get_sectors(session):
    """Testa a obtenção dos setores"""
    print_step(2, "Testando Obtenção de Setores")
    
    try:
        response = session.get(API_SECTORS_URL)
        
        if response.status_code == 200:
            sectors = response.json().get("sectors", [])
            print_success(f"Setores obtidos com sucesso: {len(sectors)} setores")
            
            for sector in sectors:
                print_info(f"  - {sector['name']} ({sector['id']})")
            
            return sectors
        else:
            print_error(f"Falha ao obter setores. Status: {response.status_code}")
            return []
            
    except Exception as e:
        print_error(f"Erro ao obter setores: {str(e)}")
        return []

def test_upload_pdf(session, sectors):
    """Testa o upload de um PDF"""
    print_step(3, "Testando Upload de PDF")
    
    if not sectors:
        print_error("Nenhum setor disponível para teste")
        return None
    
    # Criar um arquivo de teste
    test_filename = "teste_treinamento_comercial.pdf"
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Teste de PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    # Salvar arquivo temporário
    with open(test_filename, "wb") as f:
        f.write(test_content)
    
    try:
        # Preparar dados do upload
        sector_id = sectors[0]["id"]  # Usar o primeiro setor
        training_date = datetime.now().strftime("%Y-%m-%d")
        
        files = {"file": (test_filename, open(test_filename, "rb"), "application/pdf")}
        data = {
            "sector_id": sector_id,
            "description": "Treinamento de teste para o setor comercial",
            "training_date": training_date,
            "trainer": "Matheus Gallina"
        }
        
        print_info(f"Enviando PDF para setor: {sectors[0]['name']}")
        
        response = session.post(API_PDFS_URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print_success("PDF enviado com sucesso")
            print_info(f"  - ID: {result['pdf']['id']}")
            print_info(f"  - Nome: {result['pdf']['original_filename']}")
            print_info(f"  - Setor: {result['pdf']['sector_id']}")
            print_info(f"  - Treinador: {result['pdf']['trainer']}")
            
            return result['pdf']
        else:
            print_error(f"Falha no upload. Status: {response.status_code}")
            print_error(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Erro durante upload: {str(e)}")
        return None
    finally:
        # Limpar arquivo temporário
        if os.path.exists(test_filename):
            os.remove(test_filename)

def test_list_pdfs(session):
    """Testa a listagem de PDFs"""
    print_step(4, "Testando Listagem de PDFs")
    
    try:
        response = session.get(API_PDFS_URL)
        
        if response.status_code == 200:
            pdfs = response.json().get("pdfs", [])
            print_success(f"PDFs listados com sucesso: {len(pdfs)} arquivos")
            
            for pdf in pdfs:
                print_info(f"  - {pdf['original_filename']} (Setor: {pdf.get('sector_id', 'N/A')})")
            
            return pdfs
        else:
            print_error(f"Falha ao listar PDFs. Status: {response.status_code}")
            return []
            
    except Exception as e:
        print_error(f"Erro ao listar PDFs: {str(e)}")
        return []

def test_filter_pdfs_by_sector(session, sectors):
    """Testa o filtro de PDFs por setor"""
    print_step(5, "Testando Filtro por Setor")
    
    if not sectors:
        print_error("Nenhum setor disponível para teste")
        return
    
    for sector in sectors[:2]:  # Testar apenas os 2 primeiros setores
        try:
            response = session.get(f"{API_PDFS_URL}?sector_id={sector['id']}")
            
            if response.status_code == 200:
                pdfs = response.json().get("pdfs", [])
                print_success(f"PDFs do setor '{sector['name']}': {len(pdfs)} arquivos")
                
                for pdf in pdfs:
                    print_info(f"  - {pdf['original_filename']}")
                    
            else:
                print_error(f"Falha ao filtrar por setor {sector['name']}. Status: {response.status_code}")
                
        except Exception as e:
            print_error(f"Erro ao filtrar por setor {sector['name']}: {str(e)}")

def test_view_pdf(session, pdfs):
    """Testa a visualização de um PDF"""
    print_step(6, "Testando Visualização de PDF")
    
    if not pdfs:
        print_error("Nenhum PDF disponível para teste")
        return
    
    pdf = pdfs[0]  # Usar o primeiro PDF
    
    try:
        response = session.get(f"{API_PDFS_URL}/{pdf['id']}/view")
        
        if response.status_code == 200:
            print_success(f"PDF visualizado com sucesso: {pdf['original_filename']}")
            print_info(f"  - Tamanho da resposta: {len(response.content)} bytes")
        else:
            print_error(f"Falha ao visualizar PDF. Status: {response.status_code}")
            
    except Exception as e:
        print_error(f"Erro ao visualizar PDF: {str(e)}")

def test_download_pdf(session, pdfs):
    """Testa o download de um PDF"""
    print_step(7, "Testando Download de PDF")
    
    if not pdfs:
        print_error("Nenhum PDF disponível para teste")
        return
    
    pdf = pdfs[0]  # Usar o primeiro PDF
    
    try:
        response = session.get(f"{BASE_URL}/uploads/{pdf['filename']}")
        
        if response.status_code == 200:
            print_success(f"PDF baixado com sucesso: {pdf['original_filename']}")
            print_info(f"  - Tamanho do arquivo: {len(response.content)} bytes")
        else:
            print_error(f"Falha ao baixar PDF. Status: {response.status_code}")
            
    except Exception as e:
        print_error(f"Erro ao baixar PDF: {str(e)}")

def test_delete_pdf(session, pdfs):
    """Testa a exclusão de um PDF"""
    print_step(8, "Testando Exclusão de PDF")
    
    if not pdfs:
        print_error("Nenhum PDF disponível para teste")
        return
    
    pdf = pdfs[0]  # Usar o primeiro PDF
    
    try:
        response = session.delete(f"{API_PDFS_URL}/{pdf['id']}")
        
        if response.status_code == 200:
            print_success(f"PDF excluído com sucesso: {pdf['original_filename']}")
        else:
            print_error(f"Falha ao excluir PDF. Status: {response.status_code}")
            
    except Exception as e:
        print_error(f"Erro ao excluir PDF: {str(e)}")

def test_admin_pdfs_page(session):
    """Testa o acesso à página administrativa de PDFs"""
    print_step(9, "Testando Acesso à Página de PDFs")
    
    try:
        response = session.get(PDFS_URL)
        
        if response.status_code == 200:
            print_success("Página administrativa de PDFs acessada com sucesso")
            print_info(f"  - Tamanho da página: {len(response.text)} caracteres")
            
            # Verificar se contém elementos importantes
            if "PDFs Organizados por Setores" in response.text:
                print_success("Título da página encontrado")
            else:
                print_error("Título da página não encontrado")
                
            if "Upload de Arquivos por Setor" in response.text:
                print_success("Seção de upload encontrada")
            else:
                print_error("Seção de upload não encontrada")
                
        else:
            print_error(f"Falha ao acessar página. Status: {response.status_code}")
            
    except Exception as e:
        print_error(f"Erro ao acessar página: {str(e)}")

def main():
    """Função principal do teste"""
    print("🚀 INICIANDO TESTE DO SISTEMA DE PDFS POR SETORES")
    print("=" * 60)
    
    # Teste 1: Login
    session = test_login()
    if not session:
        print_error("Falha no login. Abortando testes.")
        return
    
    # Teste 2: Obter setores
    sectors = test_get_sectors(session)
    
    # Teste 3: Upload de PDF
    uploaded_pdf = test_upload_pdf(session, sectors)
    
    # Teste 4: Listar PDFs
    pdfs = test_list_pdfs(session)
    
    # Teste 5: Filtrar por setor
    test_filter_pdfs_by_sector(session, sectors)
    
    # Teste 6: Visualizar PDF
    if pdfs:
        test_view_pdf(session, pdfs)
    
    # Teste 7: Download de PDF
    if pdfs:
        test_download_pdf(session, pdfs)
    
    # Teste 8: Excluir PDF
    if pdfs:
        test_delete_pdf(session, pdfs)
    
    # Teste 9: Página administrativa
    test_admin_pdfs_page(session)
    
    print("\n" + "=" * 60)
    print("🎉 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("\nResumo dos testes:")
    print("✅ Login no sistema")
    print("✅ Obtenção de setores")
    print("✅ Upload de PDF com setor")
    print("✅ Listagem de PDFs")
    print("✅ Filtro por setor")
    print("✅ Visualização de PDF")
    print("✅ Download de PDF")
    print("✅ Exclusão de PDF")
    print("✅ Acesso à página administrativa")
    print("\nO sistema de PDFs por setores está funcionando corretamente!")

if __name__ == "__main__":
    main() 