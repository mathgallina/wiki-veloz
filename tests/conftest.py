"""
Configuração do pytest para o Wiki Veloz Fibra
"""

import shutil
import tempfile

import pytest


@pytest.fixture
def temp_data_dir():
    """Cria um diretório temporário para dados de teste"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_users():
    """Retorna dados de usuários de exemplo"""
    return [
        {
            "id": "admin-001",
            "username": "matheus.gallina",
            "name": "Matheus Gallina",
            "email": "matheus@velozfibra.com",
            "password_hash": "hashed_password",
            "role": "admin",
            "created_at": "2025-07-16T10:00:00",
            "last_login": None,
            "is_active": True,
        }
    ]


@pytest.fixture
def sample_pages():
    """Retorna dados de páginas de exemplo"""
    return [
        {
            "id": "page-001",
            "title": "Página Inicial",
            "content": "# Bem-vindo ao Wiki Veloz Fibra",
            "category": "Geral",
            "created_at": "2025-07-16T10:00:00",
            "updated_at": "2025-07-16T10:00:00",
            "created_by": "matheus.gallina",
            "is_published": True,
        }
    ]


@pytest.fixture
def sample_pdfs():
    """Retorna dados de PDFs de exemplo"""
    return [
        {
            "id": "pdf-001",
            "filename": "documento_teste.pdf",
            "original_name": "Documento Teste.pdf",
            "file_size": 1024,
            "upload_date": "2025-07-16T10:00:00",
            "uploaded_by": "matheus.gallina",
            "description": "Documento de teste",
            "tags": ["teste", "documento"],
        }
    ] 