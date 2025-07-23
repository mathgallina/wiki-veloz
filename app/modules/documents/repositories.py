"""
Repositório para persistência de dados dos documentos corporativos
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
        self.documents_file = "data/documents.json"
        self.categories_file = "data/document_categories.json"
        self.versions_file = "data/document_versions.json"
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Garante que os arquivos de dados existam"""
        os.makedirs("data", exist_ok=True)
        
        # Criar arquivo de documentos se não existir
        if not os.path.exists(self.documents_file):
            with open(self.documents_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        # Criar arquivo de categorias se não existir
        if not os.path.exists(self.categories_file):
            self._create_default_categories()
        
        # Criar arquivo de versões se não existir
        if not os.path.exists(self.versions_file):
            with open(self.versions_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _create_default_categories(self):
        """Cria categorias padrão"""
        default_categories = [
            {
                "id": "meeting-minutes",
                "name": "Atas de Reunião",
                "description": "Documentos de atas de reuniões e assembleias",
                "color": "bg-blue-500",
                "icon": "📋",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "company-rules",
                "name": "Regras da Empresa",
                "description": "Regras, normas e diretrizes corporativas",
                "color": "bg-red-500",
                "icon": "📜",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "policies",
                "name": "Políticas",
                "description": "Políticas internas e procedimentos",
                "color": "bg-green-500",
                "icon": "⚖️",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "procedures",
                "name": "Procedimentos",
                "description": "Procedimentos operacionais e manuais",
                "color": "bg-purple-500",
                "icon": "📖",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "contracts",
                "name": "Contratos",
                "description": "Contratos e acordos comerciais",
                "color": "bg-orange-500",
                "icon": "📄",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "reports",
                "name": "Relatórios",
                "description": "Relatórios gerenciais e técnicos",
                "color": "bg-indigo-500",
                "icon": "📊",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(default_categories, f, ensure_ascii=False, indent=2)
    
    def load_documents(self) -> List[Document]:
        """Carrega todos os documentos"""
        try:
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Document.from_dict(doc) for doc in data]
        except FileNotFoundError:
            return []
    
    def save_documents(self, documents: List[Document]):
        """Salva lista de documentos"""
        data = [doc.to_dict() for doc in documents]
        with open(self.documents_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_categories(self) -> List[DocumentCategory]:
        """Carrega todas as categorias"""
        try:
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [DocumentCategory(**cat) for cat in data]
        except FileNotFoundError:
            return []
    
    def save_categories(self, categories: List[DocumentCategory]):
        """Salva lista de categorias"""
        data = [cat.to_dict() for cat in categories]
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_versions(self) -> List[DocumentVersion]:
        """Carrega todas as versões"""
        try:
            with open(self.versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [DocumentVersion(**version) for version in data]
        except FileNotFoundError:
            return []
    
    def save_versions(self, versions: List[DocumentVersion]):
        """Salva lista de versões"""
        data = [version.to_dict() for version in versions]
        with open(self.versions_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        """Busca documento por ID"""
        documents = self.load_documents()
        for doc in documents:
            if doc.id == document_id:
                return doc
        return None
    
    def get_category_by_id(self, category_id: str) -> Optional[DocumentCategory]:
        """Busca categoria por ID"""
        categories = self.load_categories()
        for cat in categories:
            if cat.id == category_id:
                return cat
        return None
    
    def get_documents_by_category(self, category_id: str) -> List[Document]:
        """Busca documentos por categoria"""
        documents = self.load_documents()
        return [doc for doc in documents if doc.category_id == category_id]
    
    def get_documents_by_type(self, document_type: DocumentType) -> List[Document]:
        """Busca documentos por tipo"""
        documents = self.load_documents()
        return [doc for doc in documents if doc.document_type == document_type]
    
    def get_documents_by_status(self, status: DocumentStatus) -> List[Document]:
        """Busca documentos por status"""
        documents = self.load_documents()
        return [doc for doc in documents if doc.status == status]
    
    def get_featured_documents(self) -> List[Document]:
        """Busca documentos em destaque"""
        documents = self.load_documents()
        return [doc for doc in documents if doc.is_featured]
    
    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        """Busca documentos mais recentes"""
        documents = self.load_documents()
        documents.sort(key=lambda x: x.created_at, reverse=True)
        return documents[:limit]
    
    def search_documents(self, query: str) -> List[Document]:
        """Busca documentos por texto"""
        documents = self.load_documents()
        query = query.lower()
        
        results = []
        for doc in documents:
            if (query in doc.title.lower() or 
                query in doc.content.lower() or
                any(query in tag.lower() for tag in doc.tags)):
                results.append(doc)
        
        return results
    
    def get_document_versions(self, document_id: str) -> List[DocumentVersion]:
        """Busca versões de um documento"""
        versions = self.load_versions()
        return [v for v in versions if v.document_id == document_id]
    
    def add_document(self, document: Document):
        """Adiciona novo documento"""
        documents = self.load_documents()
        documents.append(document)
        self.save_documents(documents)
    
    def update_document(self, document: Document):
        """Atualiza documento existente"""
        documents = self.load_documents()
        for i, doc in enumerate(documents):
            if doc.id == document.id:
                documents[i] = document
                break
        self.save_documents(documents)
    
    def delete_document(self, document_id: str):
        """Remove documento"""
        documents = self.load_documents()
        documents = [doc for doc in documents if doc.id != document_id]
        self.save_documents(documents)
        
        # Remove versões associadas
        versions = self.load_versions()
        versions = [v for v in versions if v.document_id != document_id]
        self.save_versions(versions)
    
    def add_version(self, version: DocumentVersion):
        """Adiciona nova versão"""
        versions = self.load_versions()
        versions.append(version)
        self.save_versions(versions)
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos documentos"""
        documents = self.load_documents()
        categories = self.load_categories()
        
        stats = {
            "total_documents": len(documents),
            "published_documents": len([d for d in documents if d.status == DocumentStatus.PUBLISHED]),
            "draft_documents": len([d for d in documents if d.status == DocumentStatus.DRAFT]),
            "archived_documents": len([d for d in documents if d.status == DocumentStatus.ARCHIVED]),
            "expired_documents": len([d for d in documents if d.is_expired()]),
            "total_categories": len(categories),
            "total_views": sum(d.views_count for d in documents),
            "total_downloads": sum(d.downloads_count for d in documents),
            "documents_by_type": {},
            "documents_by_category": {}
        }
        
        # Estatísticas por tipo
        for doc_type in DocumentType:
            stats["documents_by_type"][doc_type.value] = len(
                [d for d in documents if d.document_type == doc_type]
            )
        
        # Estatísticas por categoria
        for cat in categories:
            stats["documents_by_category"][cat.id] = len(
                [d for d in documents if d.category_id == cat.id]
            )
        
        return stats 