"""
Page service for Wiki Veloz
CDD v2.0 - Page business logic
"""

from typing import List, Optional, Tuple

from app.core.database import ActivityLogger, DatabaseManager
from app.modules.pages.repositories.page_repository import PageRepository


class PageService:
    """Service for page operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.page_repository = PageRepository(db_manager)
        self.activity_logger = ActivityLogger(db_manager)
    
    def get_all_pages(self) -> List[dict]:
        """Get all pages"""
        return self.page_repository.load_pages()
    
    def get_page_by_id(self, page_id: str) -> Optional[dict]:
        """Get page by ID"""
        page = self.page_repository.get_page_by_id(page_id)
        if page:
            # Increment views
            self.page_repository.increment_views(page_id)
        return page
    
    def get_page_by_slug(self, slug: str) -> Optional[dict]:
        """Get page by slug"""
        page = self.page_repository.get_page_by_slug(slug)
        if page:
            # Increment views
            self.page_repository.increment_views(page['id'])
        return page
    
    def create_page(self, page_data: dict, author_id: str) -> Tuple[bool, str]:
        """Create new page"""
        # Validate page data
        is_valid, message = self.validate_page_data(page_data)
        if not is_valid:
            return False, message
        
        # Add author information
        page_data['author_id'] = author_id
        
        # Create page
        success = self.page_repository.create_page(page_data)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                author_id,
                'page_created',
                f'Página criada: {page_data.get("title", "Unknown")}'
            )
            return True, "Página criada com sucesso"
        else:
            return False, "Erro ao criar página"
    
    def update_page(self, page_id: str, updates: dict, user_id: str) -> Tuple[bool, str]:
        """Update page"""
        # Check if page exists
        page = self.page_repository.get_page_by_id(page_id)
        if not page:
            return False, "Página não encontrada"
        
        # Check permissions (only author or admin can edit)
        if page.get('author_id') != user_id:
            # TODO: Check if user is admin
            return False, "Sem permissão para editar esta página"
        
        # Validate updates
        is_valid, message = self.validate_page_updates(updates)
        if not is_valid:
            return False, message
        
        # Create version before updating
        self.page_repository.create_page_version(page_id, {
            'content': page.get('content', ''),
            'title': page.get('title', ''),
            'author_id': user_id
        })
        
        # Update page
        success = self.page_repository.update_page(page_id, updates)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                user_id,
                'page_updated',
                f'Página atualizada: {updates.get("title", page.get("title", "Unknown"))}'
            )
            return True, "Página atualizada com sucesso"
        else:
            return False, "Erro ao atualizar página"
    
    def delete_page(self, page_id: str, user_id: str) -> Tuple[bool, str]:
        """Delete page"""
        # Check if page exists
        page = self.page_repository.get_page_by_id(page_id)
        if not page:
            return False, "Página não encontrada"
        
        # Check permissions (only author or admin can delete)
        if page.get('author_id') != user_id:
            # TODO: Check if user is admin
            return False, "Sem permissão para deletar esta página"
        
        # Delete page
        success = self.page_repository.delete_page(page_id)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                user_id,
                'page_deleted',
                f'Página deletada: {page.get("title", "Unknown")}'
            )
            return True, "Página deletada com sucesso"
        else:
            return False, "Erro ao deletar página"
    
    def search_pages(self, query: str) -> List[dict]:
        """Search pages"""
        return self.page_repository.search_pages(query)
    
    def get_pages_by_category(self, category: str) -> List[dict]:
        """Get pages by category"""
        return self.page_repository.get_pages_by_category(category)
    
    def get_pages_by_author(self, author_id: str) -> List[dict]:
        """Get pages by author"""
        return self.page_repository.get_pages_by_author(author_id)
    
    def get_recent_pages(self, limit: int = 10) -> List[dict]:
        """Get recent pages"""
        return self.page_repository.get_recent_pages(limit)
    
    def get_popular_pages(self, limit: int = 10) -> List[dict]:
        """Get popular pages"""
        return self.page_repository.get_popular_pages(limit)
    
    def get_page_versions(self, page_id: str) -> List[dict]:
        """Get page versions"""
        return self.page_repository.get_page_versions(page_id)
    
    def restore_page_version(self, page_id: str, version: int, user_id: str) -> Tuple[bool, str]:
        """Restore page version"""
        # Check if page exists
        page = self.page_repository.get_page_by_id(page_id)
        if not page:
            return False, "Página não encontrada"
        
        # Check permissions
        if page.get('author_id') != user_id:
            # TODO: Check if user is admin
            return False, "Sem permissão para restaurar esta página"
        
        # Restore version
        success = self.page_repository.restore_page_version(page_id, version)
        
        if success:
            # Log activity
            self.activity_logger.log_activity(
                user_id,
                'page_version_restored',
                f'Versão {version} restaurada: {page.get("title", "Unknown")}'
            )
            return True, f"Versão {version} restaurada com sucesso"
        else:
            return False, "Erro ao restaurar versão"
    
    def get_page_analytics(self, page_id: str) -> dict:
        """Get page analytics"""
        page = self.page_repository.get_page_by_id(page_id)
        if not page:
            return {}
        
        return {
            'id': page.get('id'),
            'title': page.get('title'),
            'views': page.get('views', 0),
            'version': page.get('version', 1),
            'created_at': page.get('created_at'),
            'updated_at': page.get('updated_at'),
            'author_id': page.get('author_id'),
            'category': page.get('category'),
            'tags': page.get('tags', []),
            'versions_count': len(page.get('versions', []))
        }
    
    def validate_page_data(self, page_data: dict) -> Tuple[bool, str]:
        """Validate page data"""
        required_fields = ['title', 'content']
        
        for field in required_fields:
            if not page_data.get(field):
                return False, f'Campo obrigatório: {field}'
        
        # Validate title length
        if len(page_data.get('title', '')) < 3:
            return False, 'Título deve ter pelo menos 3 caracteres'
        
        # Validate content length
        if len(page_data.get('content', '')) < 10:
            return False, 'Conteúdo deve ter pelo menos 10 caracteres'
        
        # Check if slug already exists
        if 'slug' in page_data:
            existing_page = self.page_repository.get_page_by_slug(page_data['slug'])
            if existing_page:
                return False, 'Slug já existe'
        
        return True, 'Dados válidos'
    
    def validate_page_updates(self, updates: dict) -> Tuple[bool, str]:
        """Validate page updates"""
        if 'title' in updates and len(updates['title']) < 3:
            return False, 'Título deve ter pelo menos 3 caracteres'
        
        if 'content' in updates and len(updates['content']) < 10:
            return False, 'Conteúdo deve ter pelo menos 10 caracteres'
        
        return True, 'Dados válidos'
    
    def create_sample_pages(self) -> bool:
        """Create sample pages for testing"""
        sample_pages = [
            {
                'title': 'Bem-vindo ao Wiki Veloz',
                'content': '# Bem-vindo ao Wiki Veloz\n\nEste é o sistema de documentação colaborativa da Veloz Fibra.',
                'category': 'Geral',
                'tags': ['bem-vindo', 'introdução'],
                'author_id': 'admin-001'
            },
            {
                'title': 'Como Usar o Sistema',
                'content': '# Como Usar o Sistema\n\nGuia completo de utilização do Wiki Veloz.',
                'category': 'Documentação',
                'tags': ['guia', 'tutorial'],
                'author_id': 'admin-001'
            },
            {
                'title': 'Políticas da Empresa',
                'content': '# Políticas da Empresa\n\nDocumentação das políticas internas.',
                'category': 'Políticas',
                'tags': ['políticas', 'empresa'],
                'author_id': 'admin-001'
            }
        ]
        
        success_count = 0
        for page_data in sample_pages:
            success, _ = self.create_page(page_data, 'admin-001')
            if success:
                success_count += 1
        
        return success_count == len(sample_pages) 