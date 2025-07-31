"""
Repositório para persistência de dados dos documentos corporations
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Document,
    DocumentCategory,
    DocumentStatus,
    DocumentType,
    DocumentVersion,
)


class DocumentRepository:
    """Repositório para operações de dados dos documentos"""

    def __init__(self):
        self.data_file = "data/documents.json"
        self._ensure_data_files()

    def _ensure_data_files(self):
        """Garante que os arquivos de dados existam"""
        os.makedirs("data", exist_ok=True)

        # Criar arquivo de documentos se não existir
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def create(self, document: Document):
        """Cria um novo documento"""
        documents = self.get_all()
        documents.append(document)
        self._save_documents(documents)

    def get_by_id(self, document_id: str) -> Optional[Document]:
        """Busca documento por ID"""
        documents = self.get_all()
        for doc in documents:
            if doc.id == document_id:
                return doc
        return None

    def get_all(self) -> list[Document]:
        """Obtém todos os documentos"""
        try:
            with open(self.data_file, encoding="utf-8") as f:
                data = json.load(f)
                return [Document(**doc) for doc in data]
        except FileNotFoundError:
            return []

    def update(self, document: Document):
        """Atualiza documento existente"""
        documents = self.get_all()
        for i, doc in enumerate(documents):
            if doc.id == document.id:
                documents[i] = document
                break
        self._save_documents(documents)

    def delete(self, document_id: str) -> bool:
        """Remove documento"""
        documents = self.get_all()
        original_count = len(documents)
        documents = [doc for doc in documents if doc.id != document_id]
        self._save_documents(documents)
        return len(documents) < original_count

    def get_by_category(self, category_id: str) -> list[Document]:
        """Busca documentos por categoria"""
        documents = self.get_all()
        return [doc for doc in documents if doc.category_id == category_id]

    def get_by_type(self, document_type: str) -> list[Document]:
        """Busca documentos por tipo"""
        documents = self.get_all()
        return [doc for doc in documents if doc.type == document_type]

    def get_by_status(self, status: str) -> list[Document]:
        """Busca documentos por status"""
        documents = self.get_all()
        return [doc for doc in documents if doc.status == status]

    def search(self, query: str) -> list[Document]:
        """Busca documentos por texto"""
        documents = self.get_all()
        query = query.lower()

        results = []
        for doc in documents:
            if (
                query in doc.title.lower()
                or query in doc.description.lower()
                or query in doc.content.lower()
            ):
                results.append(doc)

        return results

    def _save_documents(self, documents: list[Document]):
        """Salva lista de documentos"""
        data = [doc.to_dict() for doc in documents]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class DocumentCategoryRepository:
    """Repositório para operações de dados das categorias"""

    def __init__(self):
        self.data_file = "data/document_categories.json"
        self._ensure_data_files()

    def _ensure_data_files(self):
        """Garante que os arquivos de dados existam"""
        os.makedirs("data", exist_ok=True)

        # Criar arquivo de categorias se não existir
        if not os.path.exists(self.data_file):
            self._create_default_categories()

    def _create_default_categories(self):
        """Cria categorias padrão"""
        default_categories = [
            {
                "id": "meeting-minutes",
                "name": "Atas de Reunião",
                "description": "Documentos de atas de reuniões e assembleias",
                "color": "#3b82f6",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "company-rules",
                "name": "Regras da Empresa",
                "description": "Regras, normas e diretrizes corporativas",
                "color": "#ef4444",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "policies",
                "name": "Políticas",
                "description": "Políticas internas e procedimentos",
                "color": "#10b981",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "procedures",
                "name": "Procedimentos",
                "description": "Procedimentos operacionais e manuais",
                "color": "#8b5cf6",
                "created_at": datetime.now().isoformat(),
            },
        ]

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(default_categories, f, ensure_ascii=False, indent=2)

    def create(self, category: DocumentCategory):
        """Cria uma nova categoria"""
        categories = self.get_all()
        categories.append(category)
        self._save_categories(categories)

    def get_by_id(self, category_id: str) -> Optional[DocumentCategory]:
        """Busca categoria por ID"""
        categories = self.get_all()
        for cat in categories:
            if cat.id == category_id:
                return cat
        return None

    def get_all(self) -> list[DocumentCategory]:
        """Obtém todas as categorias"""
        try:
            with open(self.data_file, encoding="utf-8") as f:
                data = json.load(f)
                return [DocumentCategory(**cat) for cat in data]
        except FileNotFoundError:
            return []

    def update(self, category: DocumentCategory):
        """Atualiza categoria existente"""
        categories = self.get_all()
        for i, cat in enumerate(categories):
            if cat.id == category.id:
                categories[i] = category
                break
        self._save_categories(categories)

    def delete(self, category_id: str) -> bool:
        """Remove categoria"""
        categories = self.get_all()
        original_count = len(categories)
        categories = [cat for cat in categories if cat.id != category_id]
        self._save_categories(categories)
        return len(categories) < original_count

    def _save_categories(self, categories: list[DocumentCategory]):
        """Salva lista de categorias"""
        data = [cat.to_dict() for cat in categories]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class DocumentVersionRepository:
    """Repositório para operações de dados das versões"""

    def __init__(self):
        self.data_file = "data/document_versions.json"
        self._ensure_data_files()

    def _ensure_data_files(self):
        """Garante que os arquivos de dados existam"""
        os.makedirs("data", exist_ok=True)

        # Criar arquivo de versões se não existir
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def create(self, version: DocumentVersion):
        """Cria uma nova versão"""
        versions = self.get_all()
        versions.append(version)
        self._save_versions(versions)

    def get_by_document_id(self, document_id: str) -> list[DocumentVersion]:
        """Busca versões de um documento"""
        versions = self.get_all()
        return [v for v in versions if v.document_id == document_id]

    def get_latest_version(self, document_id: str) -> Optional[DocumentVersion]:
        """Obtém a versão mais recente de um documento"""
        versions = self.get_by_document_id(document_id)
        if not versions:
            return None
        return max(versions, key=lambda v: v.version)

    def get_all(self) -> list[DocumentVersion]:
        """Obtém todas as versões"""
        try:
            with open(self.data_file, encoding="utf-8") as f:
                data = json.load(f)
                return [DocumentVersion(**version) for version in data]
        except FileNotFoundError:
            return []

    def _save_versions(self, versions: list[DocumentVersion]):
        """Salva lista de versões"""
        data = [version.to_dict() for version in versions]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
