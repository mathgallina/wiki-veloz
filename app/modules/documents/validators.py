"""
Validador para documentos corporativos
"""
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from app.modules.documents.models import DocumentPriority, DocumentStatus, DocumentType


class ValidationError(Exception):
    """Exceção para erros de validação"""
    pass


@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class SecurityValidator:
    """Validador de segurança para documentos"""
    
    @staticmethod
    def validate_xss_prevention(content: str) -> ValidationResult:
        """Valida se o conteúdo não contém scripts maliciosos"""
        errors = []
        warnings = []
        
        # Padrões suspeitos
        suspicious_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                errors.append(f"Conteúdo suspeito detectado: {pattern}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    @staticmethod
    def validate_sql_injection_prevention(content: str) -> ValidationResult:
        """Valida se o conteúdo não contém tentativas de SQL injection"""
        errors = []
        warnings = []
        
        # Padrões de SQL injection
        sql_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
            r'(\b(exec|execute)\b)',
            r'(\b(xp_cmdshell)\b)',
            r'(\b(script)\b)'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                warnings.append(f"Padrão suspeito detectado: {pattern}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class DocumentValidator:
    """Validador principal para documentos"""
    
    def __init__(self):
        self.security_validator = SecurityValidator()
    
    def validate_document_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Valida dados de um documento"""
        errors = []
        warnings = []
        
        # Validações obrigatórias
        required_fields = ['title', 'content', 'type', 'category_id']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(
                    f"Campo obrigatório ausente: {field}"
                )
        
        # Validação de título
        if 'title' in data and data['title']:
            if len(data['title']) < 3:
                errors.append("Título deve ter pelo menos 3 caracteres")
            if len(data['title']) > 200:
                errors.append("Título deve ter no máximo 200 caracteres")
        
        # Validação de conteúdo
        if 'content' in data and data['content']:
            if len(data['content']) < 10:
                errors.append("Conteúdo deve ter pelo menos 10 caracteres")
            if len(data['content']) > 50000:
                errors.append("Conteúdo deve ter no máximo 50.000 caracteres")
            
            # Validação de segurança
            security_result = self.security_validator.validate_xss_prevention(data['content'])
            errors.extend(security_result.errors)
            warnings.extend(security_result.warnings)
            
            sql_result = self.security_validator.validate_sql_injection_prevention(data['content'])
            warnings.extend(sql_result.warnings)
        
        # Validação de tipo
        if 'type' in data and data['type']:
            try:
                DocumentType(data['type'])
            except ValueError:
                errors.append(f"Tipo de documento inválido: {data['type']}")
        
        # Validação de status
        if 'status' in data and data['status']:
            try:
                DocumentStatus(data['status'])
            except ValueError:
                errors.append(f"Status inválido: {data['status']}")
        
        # Validação de prioridade
        if 'priority' in data and data['priority']:
            try:
                DocumentPriority(data['priority'])
            except ValueError:
                errors.append(f"Prioridade inválida: {data['priority']}")
        
        # Validação de categoria
        if 'category_id' in data and data['category_id']:
            if not isinstance(data['category_id'], int) or data['category_id'] <= 0:
                errors.append("ID da categoria deve ser um número positivo")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_category_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Valida dados de uma categoria"""
        errors = []
        warnings = []
        
        # Validações obrigatórias
        if 'name' not in data or not data['name']:
            errors.append("Nome da categoria é obrigatório")
        
        # Validação de nome
        if 'name' in data and data['name']:
            if len(data['name']) < 2:
                errors.append("Nome da categoria deve ter pelo menos 2 caracteres")
            if len(data['name']) > 100:
                errors.append("Nome da categoria deve ter no máximo 100 caracteres")
            
            # Validação de segurança
            security_result = self.security_validator.validate_xss_prevention(data['name'])
            errors.extend(security_result.errors)
        
        # Validação de descrição
        if 'description' in data and data['description']:
            if len(data['description']) > 500:
                errors.append("Descrição deve ter no máximo 500 caracteres")
            
            # Validação de segurança
            security_result = self.security_validator.validate_xss_prevention(data['description'])
            errors.extend(security_result.errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_search_params(self, params: Dict[str, Any]) -> ValidationResult:
        """Valida parâmetros de busca"""
        errors = []
        warnings = []
        
        # Validação de query
        if 'query' in params and params['query']:
            if len(params['query']) < 2:
                errors.append("Termo de busca deve ter pelo menos 2 caracteres")
            if len(params['query']) > 100:
                errors.append("Termo de busca deve ter no máximo 100 caracteres")
            
            # Validação de segurança
            security_result = self.security_validator.validate_xss_prevention(params['query'])
            errors.extend(security_result.errors)
        
        # Validação de filtros
        if 'type' in params and params['type']:
            try:
                DocumentType(params['type'])
            except ValueError:
                errors.append(f"Tipo de filtro inválido: {params['type']}")
        
        if 'status' in params and params['status']:
            try:
                DocumentStatus(params['status'])
            except ValueError:
                errors.append(f"Status de filtro inválido: {params['status']}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


# Instância global do validador
document_validator = DocumentValidator() 