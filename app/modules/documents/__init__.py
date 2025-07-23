"""
Módulo de Documentos Corporativos - Wiki Veloz
Gestão de atas de reuniões, regras da empresa e documentos importantes
"""

from .models import Document, DocumentCategory, DocumentVersion
from .repositories import DocumentRepository
from .services import DocumentService
from .validators import DocumentValidator

__all__ = [
    'Document',
    'DocumentCategory', 
    'DocumentVersion',
    'DocumentRepository',
    'DocumentService',
    'DocumentValidator'
] 