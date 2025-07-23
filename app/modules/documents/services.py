"""
Serviço de negócio para documentos corporativos
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Document,
    DocumentCategory,
    DocumentPriority,
    DocumentStatus,
    DocumentType,
    DocumentVersion,
)
from .repositories import DocumentRepository
from .validators import DocumentValidator


class DocumentService:
    """Serviço de negócio para documentos corporativos"""
    
    def __init__(self):
        self.repository = DocumentRepository()
        self.validator = DocumentValidator()
    
    def create_document(self, data: Dict[str, Any], author_id: str, author_name: str) -> Document:
        """Cria novo documento"""
        # Validar dados
        self.validator.validate_document_data(data)
        
        # Criar documento
        document = Document(
            id=str(uuid.uuid4()),
            title=data['title'],
            content=data['content'],
            document_type=DocumentType(data['document_type']),
            category_id=data['category_id'],
            status=DocumentStatus(data.get('status', 'draft')),
            priority=DocumentPriority(data.get('priority', 'medium')),
            author_id=author_id,
            author_name=author_name,
            tags=data.get('tags', []),
            meeting_date=datetime.fromisoformat(data['meeting_date']) if data.get('meeting_date') else None,
            meeting_participants=data.get('meeting_participants', []),
            meeting_location=data.get('meeting_location'),
            expiration_date=datetime.fromisoformat(data['expiration_date']) if data.get('expiration_date') else None,
            is_featured=data.get('is_featured', False)
        )
        
        # Salvar documento
        self.repository.add_document(document)
        
        # Criar primeira versão
        version = DocumentVersion(
            id=str(uuid.uuid4()),
            document_id=document.id,
            version_number=1,
            content=document.content,
            changes_summary="Versão inicial",
            created_by=author_id,
            created_at=datetime.now()
        )
        self.repository.add_version(version)
        
        return document
    
    def update_document(self, document_id: str, data: Dict[str, Any], user_id: str) -> Document:
        """Atualiza documento existente"""
        document = self.repository.get_document_by_id(document_id)
        if not document:
            raise ValueError("Documento não encontrado")
        
        # Validar dados
        self.validator.validate_document_update(data)
        
        # Criar nova versão se conteúdo mudou
        if data.get('content') and data['content'] != document.content:
            version = DocumentVersion(
                id=str(uuid.uuid4()),
                document_id=document.id,
                version_number=document.version + 1,
                content=data['content'],
                changes_summary=data.get('changes_summary', 'Atualização de conteúdo'),
                created_by=user_id,
                created_at=datetime.now()
            )
            self.repository.add_version(version)
            document.version += 1
        
        # Atualizar campos
        if 'title' in data:
            document.title = data['title']
        if 'content' in data:
            document.content = data['content']
        if 'document_type' in data:
            document.document_type = DocumentType(data['document_type'])
        if 'category_id' in data:
            document.category_id = data['category_id']
        if 'status' in data:
            document.status = DocumentStatus(data['status'])
        if 'priority' in data:
            document.priority = DocumentPriority(data['priority'])
        if 'tags' in data:
            document.tags = data['tags']
        if 'meeting_date' in data:
            document.meeting_date = datetime.fromisoformat(data['meeting_date']) if data['meeting_date'] else None
        if 'meeting_participants' in data:
            document.meeting_participants = data['meeting_participants']
        if 'meeting_location' in data:
            document.meeting_location = data['meeting_location']
        if 'expiration_date' in data:
            document.expiration_date = datetime.fromisoformat(data['expiration_date']) if data['expiration_date'] else None
        if 'is_featured' in data:
            document.is_featured = data['is_featured']
        
        document.updated_at = datetime.now()
        
        # Salvar alterações
        self.repository.update_document(document)
        
        return document
    
    def delete_document(self, document_id: str) -> bool:
        """Remove documento"""
        document = self.repository.get_document_by_id(document_id)
        if not document:
            return False
        
        self.repository.delete_document(document_id)
        return True
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Busca documento por ID"""
        document = self.repository.get_document_by_id(document_id)
        if document:
            document.increment_view()
            self.repository.update_document(document)
        return document
    
    def get_all_documents(self, filters: Dict[str, Any] = None) -> List[Document]:
        """Busca todos os documentos com filtros opcionais"""
        documents = self.repository.load_documents()
        
        if not filters:
            return documents
        
        # Aplicar filtros
        if filters.get('category_id'):
            documents = [d for d in documents if d.category_id == filters['category_id']]
        
        if filters.get('document_type'):
            documents = [d for d in documents if d.document_type.value == filters['document_type']]
        
        if filters.get('status'):
            documents = [d for d in documents if d.status.value == filters['status']]
        
        if filters.get('priority'):
            documents = [d for d in documents if d.priority.value == filters['priority']]
        
        if filters.get('author_id'):
            documents = [d for d in documents if d.author_id == filters['author_id']]
        
        if filters.get('featured'):
            documents = [d for d in documents if d.is_featured == filters['featured']]
        
        # Ordenação
        sort_by = filters.get('sort_by', 'created_at')
        reverse = filters.get('reverse', True)
        
        if sort_by == 'title':
            documents.sort(key=lambda x: x.title.lower(), reverse=reverse)
        elif sort_by == 'updated_at':
            documents.sort(key=lambda x: x.updated_at, reverse=reverse)
        elif sort_by == 'views':
            documents.sort(key=lambda x: x.views_count, reverse=reverse)
        else:
            documents.sort(key=lambda x: x.created_at, reverse=reverse)
        
        return documents
    
    def search_documents(self, query: str) -> List[Document]:
        """Busca documentos por texto"""
        return self.repository.search_documents(query)
    
    def get_featured_documents(self) -> List[Document]:
        """Busca documentos em destaque"""
        return self.repository.get_featured_documents()
    
    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        """Busca documentos mais recentes"""
        return self.repository.get_recent_documents(limit)
    
    def get_document_versions(self, document_id: str) -> List[DocumentVersion]:
        """Busca versões de um documento"""
        return self.repository.get_document_versions(document_id)
    
    def get_categories(self) -> List[DocumentCategory]:
        """Busca todas as categorias"""
        return self.repository.load_categories()
    
    def get_category(self, category_id: str) -> Optional[DocumentCategory]:
        """Busca categoria por ID"""
        return self.repository.get_category_by_id(category_id)
    
    def create_category(self, data: Dict[str, Any]) -> DocumentCategory:
        """Cria nova categoria"""
        self.validator.validate_category_data(data)
        
        category = DocumentCategory(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            color=data['color'],
            icon=data['icon'],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        categories = self.repository.load_categories()
        categories.append(category)
        self.repository.save_categories(categories)
        
        return category
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos documentos"""
        return self.repository.get_document_stats()
    
    def toggle_featured(self, document_id: str) -> Document:
        """Alterna status de destaque do documento"""
        document = self.repository.get_document_by_id(document_id)
        if not document:
            raise ValueError("Documento não encontrado")
        
        document.is_featured = not document.is_featured
        document.updated_at = datetime.now()
        
        self.repository.update_document(document)
        return document
    
    def publish_document(self, document_id: str) -> Document:
        """Publica documento"""
        document = self.repository.get_document_by_id(document_id)
        if not document:
            raise ValueError("Documento não encontrado")
        
        document.status = DocumentStatus.PUBLISHED
        document.updated_at = datetime.now()
        
        self.repository.update_document(document)
        return document
    
    def archive_document(self, document_id: str) -> Document:
        """Arquiva documento"""
        document = self.repository.get_document_by_id(document_id)
        if not document:
            raise ValueError("Documento não encontrado")
        
        document.status = DocumentStatus.ARCHIVED
        document.updated_at = datetime.now()
        
        self.repository.update_document(document)
        return document 