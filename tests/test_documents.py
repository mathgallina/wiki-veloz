"""
Testes unitários para o módulo de documentos corporations
"""
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.modules.documents.models import (
    Document,
    DocumentCategory,
    DocumentPriority,
    DocumentStatus,
    DocumentType,
    DocumentVersion,
)
from app.modules.documents.repositories import (
    DocumentCategoryRepository,
    DocumentRepository,
    DocumentVersionRepository,
)
from app.modules.documents.services import DocumentService
from app.modules.documents.validators import DocumentValidator


class TestDocumentModels:
    """Testes para os modelos de dados"""

    def test_document_creation(self):
        """Testa criação de documento"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        assert doc.id == "test-id"
        assert doc.title == "Test Document"
        assert doc.type == "ata"
        assert doc.status == "ativo"
        assert doc.priority == "media"

    def test_document_to_dict(self):
        """Testa conversão para dicionário"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        doc_dict = doc.to_dict()

        assert doc_dict["id"] == "test-id"
        assert doc_dict["title"] == "Test Document"
        assert doc_dict["type"] == "ata"
        assert doc_dict["status"] == "ativo"

    def test_document_category_creation(self):
        """Testa criação de categoria"""
        category = DocumentCategory(
            id="cat-1",
            name="Test Category",
            description="Test category description",
            color="#3b82f6",
            created_at="2024-01-01T00:00:00",
        )

        assert category.id == "cat-1"
        assert category.name == "Test Category"
        assert category.color == "#3b82f6"

    def test_document_version_creation(self):
        """Testa criação de versão de documento"""
        version = DocumentVersion(
            id="ver-1",
            document_id="doc-1",
            version=1,
            changes="Initial version",
            author="Test Author",
            created_at="2024-01-01T00:00:00",
        )

        assert version.id == "ver-1"
        assert version.document_id == "doc-1"
        assert version.version == 1
        assert version.changes == "Initial version"


class TestDocumentValidator:
    """Testes para o validador de documentos"""

    def setup_method(self):
        """Setup para cada teste"""
        self.validator = DocumentValidator()

    def test_validate_document_data_success(self):
        """Testa validação bem-sucedida de dados de documento"""
        data = {
            "title": "Test Document",
            "description": "Test description",
            "category_id": "cat-1",
            "type": "ata",
            "status": "ativo",
            "priority": "media",
            "content": "Test content",
        }

        result = self.validator.validate_document_data(data)

        assert result["valid"] is True
        assert "errors" not in result

    def test_validate_document_data_missing_required(self):
        """Testa validação com campos obrigatórios faltando"""
        data = {
            "description": "Test description",
            "category_id": "cat-1",
            "type": "ata",
        }

        result = self.validator.validate_document_data(data)

        assert result["valid"] is False
        assert "title" in result["errors"]

    def test_validate_document_data_invalid_type(self):
        """Testa validação com tipo inválido"""
        data = {
            "title": "Test Document",
            "description": "Test description",
            "category_id": "cat-1",
            "type": "invalid_type",
            "status": "ativo",
            "priority": "media",
            "content": "Test content",
        }

        result = self.validator.validate_document_data(data)

        assert result["valid"] is False
        assert "type" in result["errors"]

    def test_validate_document_data_xss_attempt(self):
        """Testa validação contra tentativa de XSS"""
        data = {
            "title": '<script>alert("xss")</script>',
            "description": "Test description",
            "category_id": "cat-1",
            "type": "ata",
            "status": "ativo",
            "priority": "media",
            "content": "Test content",
        }

        result = self.validator.validate_document_data(data)

        assert result["valid"] is False
        assert any("XSS" in error for error in result["errors"])

    def test_validate_category_data_success(self):
        """Testa validação bem-sucedida de dados de categoria"""
        data = {
            "name": "Test Category",
            "description": "Test category description",
            "color": "#3b82f6",
        }

        result = self.validator.validate_category_data(data)

        assert result["valid"] is True
        assert "errors" not in result

    def test_validate_category_data_missing_name(self):
        """Testa validação com nome faltando"""
        data = {"description": "Test category description", "color": "#3b82f6"}

        result = self.validator.validate_category_data(data)

        assert result["valid"] is False
        assert "name" in result["errors"]


class TestDocumentRepository:
    """Testes para o repositório de documentos"""

    def setup_method(self):
        """Setup para cada teste"""
        # Criar arquivo temporário para testes
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_file.write("[]")
        self.temp_file.close()

        self.repository = DocumentRepository()
        self.repository.data_file = self.temp_file.name

    def teardown_method(self):
        """Cleanup após cada teste"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_document(self):
        """Testa criação de documento no repositório"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        self.repository.create(doc)

        # Verificar se foi salvo
        saved_docs = self.repository.get_all()
        assert len(saved_docs) == 1
        assert saved_docs[0].id == "test-id"

    def test_get_by_id(self):
        """Testa busca de documento por ID"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        self.repository.create(doc)

        found_doc = self.repository.get_by_id("test-id")
        assert found_doc is not None
        assert found_doc.title == "Test Document"

    def test_get_by_id_not_found(self):
        """Testa busca de documento inexistente"""
        found_doc = self.repository.get_by_id("non-existent")
        assert found_doc is None

    def test_update_document(self):
        """Testa atualização de documento"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        self.repository.create(doc)

        # Atualizar documento
        doc.title = "Updated Document"
        self.repository.update(doc)

        # Verificar atualização
        updated_doc = self.repository.get_by_id("test-id")
        assert updated_doc.title == "Updated Document"

    def test_delete_document(self):
        """Testa exclusão de documento"""
        doc = Document(
            id="test-id",
            title="Test Document",
            description="Test description",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        self.repository.create(doc)

        # Verificar se existe
        assert self.repository.get_by_id("test-id") is not None

        # Excluir
        success = self.repository.delete("test-id")
        assert success is True

        # Verificar se foi excluído
        assert self.repository.get_by_id("test-id") is None

    def test_search_documents(self):
        """Testa busca de documentos"""
        doc1 = Document(
            id="test-1",
            title="Test Document 1",
            description="Test description 1",
            category_id="cat-1",
            type="ata",
            status="ativo",
            priority="media",
            content="Test content 1",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        doc2 = Document(
            id="test-2",
            title="Another Document",
            description="Another description",
            category_id="cat-1",
            type="regulamento",
            status="ativo",
            priority="media",
            content="Another content",
            author="Test Author",
            version=1,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00",
        )

        self.repository.create(doc1)
        self.repository.create(doc2)

        # Buscar por título
        results = self.repository.search("Test Document")
        assert len(results) == 1
        assert results[0].id == "test-1"

        # Buscar por conteúdo
        results = self.repository.search("Another content")
        assert len(results) == 1
        assert results[0].id == "test-2"


class TestDocumentService:
    """Testes para o serviço de documentos"""

    def setup_method(self):
        """Setup para cada teste"""
        # Criar arquivos temporários para testes
        self.temp_docs_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_docs_file.write("[]")
        self.temp_docs_file.close()

        self.temp_categories_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_categories_file.write("[]")
        self.temp_categories_file.close()

        self.temp_versions_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_versions_file.write("[]")
        self.temp_versions_file.close()

        self.temp_analytics_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_analytics_file.write(
            '{"views": {}, "downloads": {}, "daily_stats": {}, "category_stats": {}, "type_stats": {}, "user_activity": {}}'
        )
        self.temp_analytics_file.close()

        # Mock dos repositórios
        with patch("app.modules.documents.services.DocumentRepository") as mock_repo:
            with patch(
                "app.modules.documents.services.DocumentCategoryRepository"
            ) as mock_cat_repo:
                with patch(
                    "app.modules.documents.services.DocumentVersionRepository"
                ) as mock_ver_repo:
                    self.service = DocumentService()
                    self.service.repository.data_file = self.temp_docs_file.name
                    self.service.category_repository.data_file = (
                        self.temp_categories_file.name
                    )
                    self.service.version_repository.data_file = (
                        self.temp_versions_file.name
                    )
                    self.service.analytics_file = self.temp_analytics_file.name

    def teardown_method(self):
        """Cleanup após cada teste"""
        for file_path in [
            self.temp_docs_file.name,
            self.temp_categories_file.name,
            self.temp_versions_file.name,
            self.temp_analytics_file.name,
        ]:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_create_document(self):
        """Testa criação de documento via serviço"""
        data = {
            "title": "Test Document",
            "description": "Test description",
            "category_id": "cat-1",
            "type": "ata",
            "status": "ativo",
            "priority": "media",
            "content": "Test content",
            "author": "Test Author",
        }

        with patch.object(self.service.repository, "create") as mock_create:
            with patch.object(
                self.service.version_repository, "create"
            ) as mock_ver_create:
                with patch.object(self.service, "_save_analytics") as mock_save:
                    doc = self.service.create_document(data)

                    assert doc.title == "Test Document"
                    assert doc.type == "ata"
                    assert doc.status == "ativo"
                    mock_create.assert_called_once()
                    mock_ver_create.assert_called_once()
                    mock_save.assert_called_once()

    def test_get_document_analytics(self):
        """Testa obtenção de analytics de documento"""
        # Mock dos dados de analytics
        self.service.analytics = {"views": {"doc-1": 10}, "downloads": {"doc-1": 5}}

        analytics = self.service.get_document_analytics("doc-1")

        assert analytics["document_id"] == "doc-1"
        assert analytics["views"] == 10
        assert analytics["downloads"] == 5
        assert analytics["engagement_rate"] == 50.0

    def test_record_view(self):
        """Testa registro de visualização"""
        with patch.object(self.service, "_save_analytics") as mock_save:
            self.service.record_view("doc-1", "user-1")

            assert self.service.analytics["views"]["doc-1"] == 1
            mock_save.assert_called_once()

    def test_record_download(self):
        """Testa registro de download"""
        with patch.object(self.service, "_save_analytics") as mock_save:
            self.service.record_download("doc-1", "user-1")

            assert self.service.analytics["downloads"]["doc-1"] == 1
            mock_save.assert_called_once()

    def test_get_dashboard_stats(self):
        """Testa obtenção de estatísticas do dashboard"""
        # Mock de documentos e categorias
        mock_docs = [
            Document(
                id="doc-1",
                title="Doc 1",
                category_id="cat-1",
                type="ata",
                status="ativo",
            ),
            Document(
                id="doc-2",
                title="Doc 2",
                category_id="cat-1",
                type="regulamento",
                status="ativo",
            ),
        ]

        mock_categories = [DocumentCategory(id="cat-1", name="Test Category", description="Test description", color="#3b82f6")]

        with patch.object(self.service, "get_all_documents", return_value=mock_docs):
            with patch.object(
                self.service, "get_all_categories", return_value=mock_categories
            ):
                # Mock dos analytics
                self.service.analytics = {
                    "views": {"doc-1": 10, "doc-2": 5},
                    "downloads": {"doc-1": 3, "doc-2": 2},
                    "daily_stats": {},
                }

                stats = self.service.get_dashboard_stats()

                assert stats["total_documents"] == 2
                assert stats["total_views"] == 15
                assert stats["total_downloads"] == 5
                assert "status_stats" in stats
                assert "category_stats" in stats
                assert "type_stats" in stats


class TestDocumentAPI:
    """Testes para as rotas da API"""

    def setup_method(self):
        """Setup para cada teste"""
        from app import create_app

        self.app = create_app()
        self.client = self.app.test_client()

        # Mock de autenticação
        with patch("app.modules.documents.routes.login_required") as mock_auth:
            mock_auth.return_value = lambda f: f
            # Blueprint já registrado no create_app()

    def test_get_documents_api(self):
        """Testa API de listagem de documentos"""
        with patch(
            "app.modules.documents.routes.documents_service.get_all_documents"
        ) as mock_get:
            mock_get.return_value = [
                Document(
                    id="doc-1",
                    title="Test Document",
                    description="Test description",
                    category_id="cat-1",
                    type="ata",
                    status="ativo",
                    priority="media",
                    content="Test content",
                    author="Test Author",
                    version=1,
                    created_at="2024-01-01T00:00:00",
                    updated_at="2024-01-01T00:00:00",
                )
            ]

            response = self.client.get("/documents/api/documents")

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert len(data["data"]) == 1
            assert data["data"][0]["title"] == "Test Document"

    def test_create_document_api(self):
        """Testa API de criação de documento"""
        with patch(
            "app.modules.documents.routes.documents_service.create_document"
        ) as mock_create:
            mock_create.return_value = Document(
                id="doc-1",
                title="Test Document",
                description="Test description",
                category_id="cat-1",
                type="ata",
                status="ativo",
                priority="media",
                content="Test content",
                author="Test Author",
                version=1,
                created_at="2024-01-01T00:00:00",
                updated_at="2024-01-01T00:00:00",
            )

            with patch(
                "app.modules.documents.routes.validator.validate_document_data"
            ) as mock_validate:
                mock_validate.return_value = {"valid": True}

                response = self.client.post(
                    "/documents/api/documents",
                    json={
                        "title": "Test Document",
                        "description": "Test description",
                        "category_id": "cat-1",
                        "type": "ata",
                        "status": "ativo",
                        "priority": "media",
                        "content": "Test content",
                    },
                )

                assert response.status_code == 201
                data = json.loads(response.data)
                assert data["success"] is True
                assert data["data"]["title"] == "Test Document"

    def test_create_document_api_validation_error(self):
        """Testa API de criação com error de validação"""
        with patch(
            "app.modules.documents.routes.validator.validate_document_data"
        ) as mock_validate:
            mock_validate.return_value = {"valid": False, "errors": "Title is required"}

            response = self.client.post(
                "/documents/api/documents",
                json={
                    "description": "Test description",
                    "category_id": "cat-1",
                    "type": "ata",
                },
            )

            assert response.status_code == 400
            data = json.loads(response.data)
            assert data["success"] is False
            assert "Title is required" in data["message"]

    def test_get_document_analytics_api(self):
        """Testa API de analytics de documento"""
        with patch(
            "app.modules.documents.routes.documents_service.get_document_analytics"
        ) as mock_analytics:
            mock_analytics.return_value = {
                "document_id": "doc-1",
                "views": 10,
                "downloads": 5,
                "engagement_rate": 50.0,
            }

            response = self.client.get("/documents/api/documents/doc-1/analytics")

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["data"]["views"] == 10
            assert data["data"]["downloads"] == 5
            assert data["data"]["engagement_rate"] == 50.0

    def test_record_view_api(self):
        """Testa API de registro de visualização"""
        with patch(
            "app.modules.documents.routes.documents_service.record_view"
        ) as mock_record:
            response = self.client.post("/documents/api/documents/doc-1/view")

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            mock_record.assert_called_once_with("doc-1", None)

    def test_record_download_api(self):
        """Testa API de registro de download"""
        with patch(
            "app.modules.documents.routes.documents_service.record_download"
        ) as mock_record:
            response = self.client.post("/documents/api/documents/doc-1/download")

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            mock_record.assert_called_once_with("doc-1", None)


class TestDocumentIntegration:
    """Testes de integração para o módulo de documentos"""

    def setup_method(self):
        """Setup para cada teste"""
        # Criar arquivos temporários para testes de integração
        self.temp_docs_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_docs_file.write("[]")
        self.temp_docs_file.close()

        self.temp_categories_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_categories_file.write("[]")
        self.temp_categories_file.close()

        self.temp_versions_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_versions_file.write("[]")
        self.temp_versions_file.close()

        self.temp_analytics_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_analytics_file.write(
            '{"views": {}, "downloads": {}, "daily_stats": {}, "category_stats": {}, "type_stats": {}, "user_activity": {}}'
        )
        self.temp_analytics_file.close()

    def teardown_method(self):
        """Cleanup após cada teste"""
        for file_path in [
            self.temp_docs_file.name,
            self.temp_categories_file.name,
            self.temp_versions_file.name,
            self.temp_analytics_file.name,
        ]:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_full_document_lifecycle(self):
        """Testa ciclo completo de vida de um documento"""
        # Configurar repositórios
        docs_repo = DocumentRepository()
        docs_repo.data_file = self.temp_docs_file.name

        cats_repo = DocumentCategoryRepository()
        cats_repo.data_file = self.temp_categories_file.name

        vers_repo = DocumentVersionRepository()
        vers_repo.data_file = self.temp_versions_file.name

        # Criar categoria
        category = DocumentCategory(
            id="cat-1",
            name="Test Category",
            description="Test category description",
            color="#3b82f6",
            created_at="2024-01-01T00:00:00",
        )
        cats_repo.create(category)

        # Criar documento
        doc_data = {
            "title": "Test Document",
            "description": "Test description",
            "category_id": "cat-1",
            "type": "ata",
            "status": "ativo",
            "priority": "media",
            "content": "Test content",
            "author": "Test Author",
        }

        service = DocumentService()
        service.repository = docs_repo
        service.category_repository = cats_repo
        service.version_repository = vers_repo
        service.analytics_file = self.temp_analytics_file.name

        # Criar documento
        doc = service.create_document(doc_data)
        assert doc.title == "Test Document"
        assert doc.type == "ata"

        # Verificar se foi salvo
        saved_doc = docs_repo.get_by_id(doc.id)
        assert saved_doc is not None
        assert saved_doc.title == "Test Document"

        # Verificar versão inicial
        versions = vers_repo.get_by_document_id(doc.id)
        assert len(versions) == 1
        assert versions[0].version == 1

        # Atualizar documento
        update_data = {
            "title": "Updated Document",
            "description": "Updated description",
            "content": "Updated content",
            "author": "Test Author",
        }

        updated_doc = service.update_document(doc.id, update_data)
        assert updated_doc.title == "Updated Document"

        # Verificar nova versão
        versions = vers_repo.get_by_document_id(doc.id)
        assert len(versions) == 2
        assert versions[1].version == 2

        # Registrar analytics
        service.record_view(doc.id, "user-1")
        service.record_download(doc.id, "user-1")

        analytics = service.get_document_analytics(doc.id)
        assert analytics["views"] == 1
        assert analytics["downloads"] == 1

        # Excluir documento
        success = service.delete_document(doc.id)
        assert success is True

        # Verificar se foi excluído
        deleted_doc = docs_repo.get_by_id(doc.id)
        assert deleted_doc is None


if __name__ == "__main__":
    pytest.main([__file__])
