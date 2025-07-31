"""
Document service for Wiki Veloz
CDD v2.0 - Document business logic
"""

import os
from typing import List, Optional, Tuple

from app.core.database import ActivityLogger, DatabaseManager
from app.modules.documents.repositories.document_repository import DocumentRepository


class DocumentService:
    """Service for document operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.document_repository = DocumentRepository(db_manager)
        self.activity_logger = ActivityLogger(db_manager)
    
    def get_all_documents(self) -> List[dict]:
        """Get all documents"""
        return self.document_repository.load_documents()
    
    def get_document_by_id(self, document_id: str) -> Optional[dict]:
        """Get document by ID"""
        document = self.document_repository.get_document_by_id(document_id)
        if document:
            # Increment downloads when accessed
            self.document_repository.increment_downloads(document_id)
        return document
    
    def create_document(self, document_data: dict, file, author_id: str) -> Tuple[bool, str]:
        """Create new document with file upload"""
        # Validate document data
        is_valid, message = self.validate_document_data(document_data)
        if not is_valid:
            return False, message
        
        # Validate file upload
        if file:
            is_valid, message = self.document_repository.validate_file_upload(
                file.filename, 
                len(file.read())
            )
            file.seek(0)  # Reset file pointer
            if not is_valid:
                return False, message
        
        # Add author information
        document_data['author_id'] = author_id
        document_data['original_filename'] = file.filename if file else None
        
        # Save file if provided
        sanitized_filename = ""
        if file:
            sanitized_filename = self.document_repository.save_uploaded_file(file, file.filename)
            if not sanitized_filename:
                return False, "Erro ao salvar arquivo"
            document_data['filename'] = sanitized_filename
        else:
            document_data['filename'] = None
        
        # Create document
        success = self.document_repository.create_document(document_data, "")
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                author_id,
                'document_created',
                f'Documento criado: {document_data.get("title", "Unknown")}'
            )
            return True, "Documento criado com sucesso"
        else:
            return False, "Erro ao criar documento"
    
    def create_document_json(self, document_data: dict) -> Tuple[bool, str]:
        """Create new document via JSON (without file)"""
        # Validate document data
        is_valid, message = self.validate_document_data(document_data)
        if not is_valid:
            return False, message
        
        # Add required fields if not present
        if 'id' not in document_data:
            document_data['id'] = self.document_repository.generate_document_id()
        
        # Create document without file
        success = self.document_repository.create_document(document_data, "")
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                document_data.get('author', 'system'),
                'document_created',
                f'Documento criado: {document_data.get("title", "Unknown")}'
            )
            return True, "Documento criado com sucesso"
        else:
            return False, "Erro ao criar documento"
    
    def update_document(self, document_id: str, updates: dict, user_id: str) -> Tuple[bool, str]:
        """Update document"""
        # Check if document exists
        document = self.document_repository.get_document_by_id(document_id)
        if not document:
            return False, "Documento não encontrado"
        
        # Check permissions (only author or admin can edit)
        if document.get('author_id') != user_id:
            # TODO: Check if user is admin
            return False, "Sem permissão para editar este documento"
        
        # Validate updates
        is_valid, message = self.validate_document_updates(updates)
        if not is_valid:
            return False, message
        
        # Update document
        success = self.document_repository.update_document(document_id, updates)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                user_id,
                'document_updated',
                f'Documento atualizado: {updates.get("title", document.get("title", "Unknown"))}'
            )
            return True, "Documento atualizado com sucesso"
        else:
            return False, "Erro ao atualizar documento"
    
    def delete_document(self, document_id: str, user_id: str) -> Tuple[bool, str]:
        """Delete document"""
        # Check if document exists
        document = self.document_repository.get_document_by_id(document_id)
        if not document:
            return False, "Documento não encontrado"
        
        # Check permissions (author or admin can delete)
        if document.get('author_id') != user_id:
            # Check if user is admin
            from app.modules.auth.services.auth_service import AuthService
            auth_service = AuthService(self.db_manager)
            user_data = auth_service.get_user_by_id(user_id)
            
            if not user_data or user_data.get('role') != 'admin':
                return False, "Sem permissão para deletar este documento"
        
        # Delete document
        success = self.document_repository.delete_document(document_id)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                user_id,
                'document_deleted',
                f'Documento deletado: {document.get("title", "Unknown")}'
            )
            return True, "Documento deletado com sucesso"
        else:
            return False, "Erro ao deletar documento"
    
    def search_documents(self, query: str) -> List[dict]:
        """Search documents"""
        return self.document_repository.search_documents(query)
    
    def get_documents_by_category(self, category: str) -> List[dict]:
        """Get documents by category"""
        return self.document_repository.get_documents_by_category(category)
    
    def get_documents_by_author(self, author_id: str) -> List[dict]:
        """Get documents by author"""
        return self.document_repository.get_documents_by_author(author_id)
    
    def get_documents_by_page(self, page_id: str) -> List[dict]:
        """Get documents by associated page"""
        return self.document_repository.get_documents_by_page(page_id)
    
    def get_recent_documents(self, limit: int = 10) -> List[dict]:
        """Get recent documents"""
        return self.document_repository.get_recent_documents(limit)
    
    def get_popular_documents(self, limit: int = 10) -> List[dict]:
        """Get popular documents"""
        return self.document_repository.get_popular_documents(limit)
    
    def download_document(self, document_id: str, user_id: str) -> Tuple[bool, str, Optional[str]]:
        """Download document"""
        document = self.document_repository.get_document_by_id(document_id)
        if not document:
            return False, "Documento não encontrado", None
        
        file_path = self.document_repository.get_document_file_path(document_id)
        if not file_path:
            return False, "Arquivo não encontrado", None
        
        # Increment downloads
        self.document_repository.increment_downloads(document_id)
        
        # Log activity
        self.activity_logger.log_activity(
            user_id,
            'document_downloaded',
            f'Documento baixado: {document.get("title", "Unknown")}'
        )
        
        return True, document.get('filename', ''), file_path
    
    def get_document_analytics(self, document_id: str) -> dict:
        """Get document analytics"""
        return self.document_repository.get_document_analytics(document_id)
    
    def get_document_file_path(self, document_id: str) -> Optional[str]:
        """Get document file path"""
        return self.document_repository.get_document_file_path(document_id)
    
    def get_storage_analytics(self) -> dict:
        """Get storage analytics"""
        return self.document_repository.get_storage_analytics()
    
    def validate_document_data(self, document_data: dict) -> Tuple[bool, str]:
        """Validate document data"""
        required_fields = ['title', 'category']
        
        for field in required_fields:
            if not document_data.get(field):
                return False, f'Campo obrigatório: {field}'
        
        # Validate title length
        if len(document_data.get('title', '')) < 3:
            return False, 'Título deve ter pelo menos 3 caracteres'
        
        # Validate description length
        description = document_data.get('description', '')
        if description and len(description) < 10:
            return False, 'Descrição deve ter pelo menos 10 caracteres'
        
        # Validate category
        valid_categories = [
            'Geral', 'Documentação', 'Políticas', 'Técnico', 
            'Financeiro', 'RH', 'Marketing', 'Vendas'
        ]
        if document_data.get('category') not in valid_categories:
            return False, 'Categoria inválida'
        
        return True, 'Dados válidos'
    
    def validate_document_updates(self, updates: dict) -> Tuple[bool, str]:
        """Validate document updates"""
        if 'title' in updates and len(updates['title']) < 3:
            return False, 'Título deve ter pelo menos 3 caracteres'
        
        if 'description' in updates and len(updates['description']) < 10:
            return False, 'Descrição deve ter pelo menos 10 caracteres'
        
        if 'category' in updates:
            valid_categories = [
                'Geral', 'Documentação', 'Políticas', 'Técnico', 
                'Financeiro', 'RH', 'Marketing', 'Vendas'
            ]
            if updates['category'] not in valid_categories:
                return False, 'Categoria inválida'
        
        return True, 'Dados válidos'
    
    def create_sample_documents(self) -> bool:
        """Create sample documents for testing"""
        sample_documents = [
            {
                'title': 'Manual do Colaborador',
                'description': 'Manual completo com políticas e procedimentos da empresa',
                'category': 'Documentação',
                'tags': ['manual', 'colaborador', 'políticas'],
                'author_id': 'admin-001'
            },
            {
                'title': 'Procedimentos de Segurança',
                'description': 'Documento com procedimentos de segurança da empresa',
                'category': 'Políticas',
                'tags': ['segurança', 'procedimentos'],
                'author_id': 'admin-001'
            },
            {
                'title': 'Relatório Mensal',
                'description': 'Relatório de atividades do mês anterior',
                'category': 'Geral',
                'tags': ['relatório', 'mensal'],
                'author_id': 'admin-001'
            }
        ]
        
        success_count = 0
        for doc_data in sample_documents:
            success, _ = self.create_document(doc_data, None, 'admin-001')
            if success:
                success_count += 1
        
        return success_count == len(sample_documents)

    def confirm_document_read(self, document_id: str, user_id: str, ip_address: str = None) -> Tuple[bool, str]:
        """Confirm document read by user"""
        try:
            # Check if document exists
            document = self.get_document_by_id(document_id)
            if not document:
                return False, "Documento não encontrado"
            
            # Check if user already confirmed this document
            existing_confirmation = self.get_document_confirmation(document_id, user_id)
            if existing_confirmation:
                return False, "Usuário já confirmou a leitura deste documento"
            
            # Create confirmation record
            confirmation_data = {
                'id': self.document_repository.generate_confirmation_id(),
                'document_id': document_id,
                'user_id': user_id,
                'confirmed_at': self.document_repository.get_current_timestamp(),
                'ip_address': ip_address
            }
            
            success = self.document_repository.save_confirmation(confirmation_data)
            
            if success:
                # Log activity
                self.activity_logger.log_activity(
                    user_id,
                    'document_confirmed',
                    f'Leitura confirmada: {document.get("title", "Unknown")}'
                )
                return True, confirmation_data['confirmed_at']
            else:
                return False, "Erro ao salvar confirmação"
                
        except Exception as e:
            print(f"Erro ao confirmar leitura: {e}")
            return False, f"Erro interno: {str(e)}"

    def get_document_confirmation(self, document_id: str, user_id: str) -> Optional[dict]:
        """Get document confirmation for specific user"""
        try:
            return self.document_repository.get_confirmation(document_id, user_id)
        except Exception as e:
            print(f"Erro ao buscar confirmação: {e}")
            return None

    def get_document_confirmations(self, document_id: str) -> List[dict]:
        """Get all confirmations for a document"""
        try:
            return self.document_repository.get_document_confirmations(document_id)
        except Exception as e:
            print(f"Erro ao buscar confirmações: {e}")
            return []

    def get_user_confirmations(self, user_id: str) -> List[dict]:
        """Get all confirmations by a user"""
        try:
            return self.document_repository.get_user_confirmations(user_id)
        except Exception as e:
            print(f"Erro ao buscar confirmações do usuário: {e}")
            return [] 