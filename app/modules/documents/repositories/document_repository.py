"""
Document repository for Wiki Veloz
CDD v2.0 - Document data management
"""

import os
import re
import uuid
from datetime import datetime
from typing import List, Optional

from werkzeug.utils import secure_filename

from app.core.database import DatabaseManager


class DocumentRepository:
    """Repository for document operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.filename = "documents.json"
        # Use relative path from project root
        self.upload_folder = "app/static/uploads/documents"
        self._ensure_upload_folder()
    
    def _ensure_upload_folder(self):
        """Ensure upload folder exists"""
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove accents and special characters
        import unicodedata

        # Normalize unicode characters
        filename = unicodedata.normalize('NFD', filename)
        filename = ''.join(c for c in filename if not unicodedata.combining(c))
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove parentheses and other special characters
        filename = re.sub(r'[\(\)\[\]\{\}]', '', filename)
        
        # Replace multiple underscores with single underscore
        filename = re.sub(r'_+', '_', filename)
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        # Use secure_filename as final step
        sanitized = secure_filename(filename)
        
        # If secure_filename returns empty, use a default
        if not sanitized:
            sanitized = f"document_{uuid.uuid4().hex[:8]}"
        
        return sanitized
    
    def generate_document_id(self) -> str:
        """Generate unique document ID"""
        return f"doc-{uuid.uuid4().hex[:8]}"
    
    def load_documents(self) -> List[dict]:
        """Load all documents"""
        return self.db_manager.load_data(self.filename)
    
    def save_documents(self, documents: List[dict]) -> bool:
        """Save all documents"""
        return self.db_manager.save_data(self.filename, documents)
    
    def get_document_by_id(self, document_id: str) -> Optional[dict]:
        """Get document by ID"""
        return self.db_manager.get_by_id(self.filename, document_id)
    
    def get_document_by_filename(self, filename: str) -> Optional[dict]:
        """Get document by filename"""
        documents = self.load_documents()
        return next((d for d in documents if d.get('filename') == filename), None)
    
    def create_document(self, document_data: dict, file_path: str = None) -> bool:
        """Create new document"""
        documents = self.load_documents()
        
        # Generate ID if not provided
        if 'id' not in document_data:
            document_data['id'] = f"doc-{uuid.uuid4().hex[:8]}"
        
        # Add timestamps
        document_data['created_at'] = datetime.now().isoformat()
        document_data['updated_at'] = datetime.now().isoformat()
        document_data['version'] = 1
        document_data['downloads'] = 0
        
        # Add file information
        if file_path and os.path.exists(file_path):
            document_data['file_size'] = os.path.getsize(file_path)
            document_data['file_exists'] = True
        else:
            document_data['file_size'] = 0
            document_data['file_exists'] = False
        
        documents.append(document_data)
        return self.save_documents(documents)
    
    def update_document(self, document_id: str, updates: dict) -> bool:
        """Update document"""
        documents = self.load_documents()
        
        for document in documents:
            if document.get('id') == document_id:
                # Update version
                current_version = document.get('version', 1)
                updates['version'] = current_version + 1
                updates['updated_at'] = datetime.now().isoformat()
                
                document.update(updates)
                return self.save_documents(documents)
        
        return False
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document and its file"""
        document = self.get_document_by_id(document_id)
        if document:
            # Delete physical file
            filename = document.get('filename')
            if filename:  # Only try to delete if filename exists
                file_path = os.path.join(self.upload_folder, filename)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
        
        return self.db_manager.delete_item(self.filename, document_id)
    
    def get_documents_by_category(self, category: str) -> List[dict]:
        """Get documents by category"""
        documents = self.load_documents()
        return [d for d in documents if d.get('category') == category]
    
    def get_documents_by_author(self, author_id: str) -> List[dict]:
        """Get documents by author"""
        documents = self.load_documents()
        return [d for d in documents if d.get('author_id') == author_id]
    
    def get_documents_by_page(self, page_id: str) -> List[dict]:
        """Get documents by associated page"""
        documents = self.load_documents()
        return [d for d in documents if d.get('page_id') == page_id]
    
    def search_documents(self, query: str) -> List[dict]:
        """Search documents by title, description, or tags"""
        documents = self.load_documents()
        query_lower = query.lower()
        
        results = []
        for document in documents:
            # Search in title
            if query_lower in document.get('title', '').lower():
                results.append(document)
                continue
            
            # Search in description
            if query_lower in document.get('description', '').lower():
                results.append(document)
                continue
            
            # Search in tags
            tags = document.get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                results.append(document)
                continue
        
        return results
    
    def get_recent_documents(self, limit: int = 10) -> List[dict]:
        """Get recent documents"""
        documents = self.load_documents()
        sorted_documents = sorted(
            documents, 
            key=lambda x: x.get('updated_at', ''), 
            reverse=True
        )
        return sorted_documents[:limit]
    
    def get_popular_documents(self, limit: int = 10) -> List[dict]:
        """Get popular documents by downloads"""
        documents = self.load_documents()
        sorted_documents = sorted(
            documents, 
            key=lambda x: x.get('downloads', 0), 
            reverse=True
        )
        return sorted_documents[:limit]
    
    def increment_downloads(self, document_id: str) -> bool:
        """Increment document downloads"""
        documents = self.load_documents()
        
        for document in documents:
            if document.get('id') == document_id:
                current_downloads = document.get('downloads', 0)
                document['downloads'] = current_downloads + 1
                return self.save_documents(documents)
        
        return False
    
    def get_document_file_path(self, document_id: str) -> Optional[str]:
        """Get document file path with error handling"""
        document = self.get_document_by_id(document_id)
        if not document:
            print(f"Document not found: {document_id}")
            return None
            
        filename = document.get('filename')
        if not filename:
            print(f"Document has no filename: {document_id}")
            return None
            
        # Ensure upload folder exists
        self._ensure_upload_folder()
        
        # Get absolute path
        import os
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, self.upload_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
            
        return file_path
    
    def validate_file_upload(self, filename: str, file_size: int) -> tuple[bool, str]:
        """Validate file upload"""
        # Check file extension
        allowed_extensions = {
            'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 
            'xls', 'xlsx', 'csv', 'ppt', 'pptx',
            'jpg', 'jpeg', 'png', 'gif', 'bmp'
        }
        
        file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if file_ext not in allowed_extensions:
            return False, f'Extensão não permitida: {file_ext}'
        
        # Check file size (50MB max)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            return False, 'Arquivo muito grande (máximo 50MB)'
        
        # Check if filename already exists
        existing_doc = self.get_document_by_filename(filename)
        if existing_doc:
            return False, 'Arquivo com este nome já existe'
        
        return True, 'Arquivo válido'
    
    def save_uploaded_file(self, file, original_filename: str) -> str:
        """Save uploaded file with sanitized filename"""
        # Sanitize the filename
        sanitized_filename = self.sanitize_filename(original_filename)
        
        # Ensure upload folder exists
        self._ensure_upload_folder()
        
        # Create full file path
        file_path = os.path.join(self.upload_folder, sanitized_filename)
        
        try:
            file.save(file_path)
            print(f"File saved: {original_filename} -> {sanitized_filename}")
            return sanitized_filename  # Return sanitized filename for storage
        except Exception as e:
            print(f"Error saving file: {e}")
            return ""
    
    def get_document_analytics(self, document_id: str) -> dict:
        """Get document analytics"""
        document = self.get_document_by_id(document_id)
        if not document:
            return {}
        
        return {
            'id': document.get('id'),
            'title': document.get('title'),
            'downloads': document.get('downloads', 0),
            'version': document.get('version', 1),
            'created_at': document.get('created_at'),
            'updated_at': document.get('updated_at'),
            'author_id': document.get('author_id'),
            'category': document.get('category'),
            'tags': document.get('tags', []),
            'file_size': document.get('file_size', 0),
            'file_exists': document.get('file_exists', False)
        }
    
    def get_storage_analytics(self) -> dict:
        """Get storage analytics"""
        documents = self.load_documents()
        
        total_files = len(documents)
        total_size = sum(d.get('file_size', 0) for d in documents)
        existing_files = sum(1 for d in documents if d.get('file_exists', False))
        
        # Calculate size by category
        size_by_category = {}
        for doc in documents:
            category = doc.get('category', 'Sem categoria')
            size = doc.get('file_size', 0)
            size_by_category[category] = size_by_category.get(category, 0) + size
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'existing_files': existing_files,
            'missing_files': total_files - existing_files,
            'size_by_category': size_by_category
        }

    def generate_confirmation_id(self) -> str:
        """Generate unique confirmation ID"""
        return f"conf-{uuid.uuid4().hex[:8]}"

    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()

    def save_confirmation(self, confirmation_data: dict) -> bool:
        """Save document confirmation"""
        try:
            confirmations = self.db_manager.load_data("document_confirmations.json")
            confirmations.append(confirmation_data)
            return self.db_manager.save_data("document_confirmations.json", confirmations)
        except Exception as e:
            print(f"Erro ao salvar confirmação: {e}")
            return False

    def get_confirmation(self, document_id: str, user_id: str) -> Optional[dict]:
        """Get confirmation for specific document and user"""
        try:
            confirmations = self.db_manager.load_data("document_confirmations.json")
            return next(
                (c for c in confirmations 
                 if c.get('document_id') == document_id and c.get('user_id') == user_id),
                None
            )
        except Exception as e:
            print(f"Erro ao buscar confirmação: {e}")
            return None

    def get_document_confirmations(self, document_id: str) -> List[dict]:
        """Get all confirmations for a document"""
        try:
            confirmations = self.db_manager.load_data("document_confirmations.json")
            return [c for c in confirmations if c.get('document_id') == document_id]
        except Exception as e:
            print(f"Erro ao buscar confirmações do documento: {e}")
            return []

    def get_user_confirmations(self, user_id: str) -> List[dict]:
        """Get all confirmations by a user"""
        try:
            confirmations = self.db_manager.load_data("document_confirmations.json")
            return [c for c in confirmations if c.get('user_id') == user_id]
        except Exception as e:
            print(f"Erro ao buscar confirmações do usuário: {e}")
            return [] 