"""
Validador para documentos corporativos
"""
from typing import Any, Dict

from .models import DocumentPriority, DocumentStatus, DocumentType


class DocumentValidator:
    """Validador para documentos corporativos"""
    
    def validate_document_data(self, data: Dict[str, Any]):
        """Valida dados de criação de documento"""
        required_fields = ['title', 'content', 'document_type', 'category_id']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório: {field}")
        
        # Validar tipo de documento
        try:
            DocumentType(data['document_type'])
        except ValueError:
            raise ValueError("Tipo de documento inválido")
        
        # Validar status se fornecido
        if 'status' in data:
            try:
                DocumentStatus(data['status'])
            except ValueError:
                raise ValueError("Status inválido")
        
        # Validar prioridade se fornecida
        if 'priority' in data:
            try:
                DocumentPriority(data['priority'])
            except ValueError:
                raise ValueError("Prioridade inválida")
        
        # Validar título
        if len(data['title']) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        
        if len(data['title']) > 200:
            raise ValueError("Título deve ter no máximo 200 caracteres")
        
        # Validar conteúdo
        if len(data['content']) < 10:
            raise ValueError("Conteúdo deve ter pelo menos 10 caracteres")
        
        # Validar tags
        if 'tags' in data and not isinstance(data['tags'], list):
            raise ValueError("Tags deve ser uma lista")
        
        # Validar participantes se for ata de reunião
        if data['document_type'] == 'meeting_minutes':
            if 'meeting_participants' in data and not isinstance(data['meeting_participants'], list):
                raise ValueError("Participantes deve ser uma lista")
    
    def validate_document_update(self, data: Dict[str, Any]):
        """Valida dados de atualização de documento"""
        if not data:
            raise ValueError("Dados de atualização não fornecidos")
        
        # Validar campos opcionais se fornecidos
        if 'title' in data:
            if len(data['title']) < 3:
                raise ValueError("Título deve ter pelo menos 3 caracteres")
            
            if len(data['title']) > 200:
                raise ValueError("Título deve ter no máximo 200 caracteres")
        
        if 'content' in data:
            if len(data['content']) < 10:
                raise ValueError("Conteúdo deve ter pelo menos 10 caracteres")
        
        if 'document_type' in data:
            try:
                DocumentType(data['document_type'])
            except ValueError:
                raise ValueError("Tipo de documento inválido")
        
        if 'status' in data:
            try:
                DocumentStatus(data['status'])
            except ValueError:
                raise ValueError("Status inválido")
        
        if 'priority' in data:
            try:
                DocumentPriority(data['priority'])
            except ValueError:
                raise ValueError("Prioridade inválida")
        
        if 'tags' in data and not isinstance(data['tags'], list):
            raise ValueError("Tags deve ser uma lista")
    
    def validate_category_data(self, data: Dict[str, Any]):
        """Valida dados de categoria"""
        required_fields = ['id', 'name', 'description', 'color', 'icon']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório: {field}")
        
        # Validar ID
        if len(data['id']) < 3:
            raise ValueError("ID deve ter pelo menos 3 caracteres")
        
        if len(data['id']) > 50:
            raise ValueError("ID deve ter no máximo 50 caracteres")
        
        # Validar nome
        if len(data['name']) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        
        if len(data['name']) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
        
        # Validar descrição
        if len(data['description']) < 10:
            raise ValueError("Descrição deve ter pelo menos 10 caracteres")
        
        if len(data['description']) > 500:
            raise ValueError("Descrição deve ter no máximo 500 caracteres")
        
        # Validar cor
        if not data['color'].startswith('bg-'):
            raise ValueError("Cor deve começar com 'bg-'")
        
        # Validar ícone
        if len(data['icon']) < 1:
            raise ValueError("Ícone é obrigatório")
    
    def validate_search_query(self, query: str):
        """Valida query de busca"""
        if not query or len(query.strip()) < 2:
            raise ValueError("Query de busca deve ter pelo menos 2 caracteres")
        
        if len(query) > 100:
            raise ValueError("Query de busca deve ter no máximo 100 caracteres") 