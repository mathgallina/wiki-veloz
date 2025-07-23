"""
Modelos de dados para Documentos Corporativos
"""
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DocumentType(Enum):
    """Tipos de documentos corporativos"""
    ATA = "ata"                           # Ata de reunião
    REGULAMENTO = "regulamento"           # Regulamento
    POLITICA = "politica"                 # Política
    PROCEDIMENTO = "procedimento"         # Procedimento
    MANUAL = "manual"                     # Manual
    OUTRO = "outro"                       # Outros


class DocumentStatus(Enum):
    """Status dos documentos"""
    ATIVO = "ativo"           # Ativo
    RASCUNHO = "rascunho"     # Rascunho
    ARQUIVADO = "arquivado"   # Arquivado


class DocumentPriority(Enum):
    """Prioridade dos documentos"""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


@dataclass
class DocumentCategory:
    """Categoria de documento"""
    id: str
    name: str
    description: str
    color: str
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentVersion:
    """Versão de um documento"""
    id: str
    document_id: str
    version: int
    changes: str
    author: str
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Document:
    """Modelo principal de documento corporativo"""
    id: str
    title: str
    description: str
    category_id: str
    type: str
    status: str
    priority: str
    content: str
    author: str
    version: int
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self) 