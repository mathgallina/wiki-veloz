"""
Modelos de dados para Documentos Corporativos
"""
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DocumentType(Enum):
    """Tipos de documentos corporativos"""
    MEETING_MINUTES = "meeting_minutes"  # Atas de reunião
    COMPANY_RULES = "company_rules"      # Regras da empresa
    POLICIES = "policies"                # Políticas
    PROCEDURES = "procedures"            # Procedimentos
    CONTRACTS = "contracts"              # Contratos
    REPORTS = "reports"                  # Relatórios
    OTHER = "other"                      # Outros


class DocumentStatus(Enum):
    """Status dos documentos"""
    DRAFT = "draft"           # Rascunho
    PUBLISHED = "published"   # Publicado
    ARCHIVED = "archived"     # Arquivado
    EXPIRED = "expired"       # Expirado


class DocumentPriority(Enum):
    """Prioridade dos documentos"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DocumentCategory:
    """Categoria de documento"""
    id: str
    name: str
    description: str
    color: str
    icon: str
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentVersion:
    """Versão de um documento"""
    id: str
    document_id: str
    version_number: int
    content: str
    changes_summary: str
    created_by: str
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Document:
    """Modelo principal de documento corporativo"""
    id: str
    title: str
    content: str
    document_type: DocumentType
    category_id: str
    status: DocumentStatus
    priority: DocumentPriority
    author_id: str
    author_name: str
    tags: List[str]
    meeting_date: Optional[datetime] = None
    meeting_participants: List[str] = None
    meeting_location: Optional[str] = None
    expiration_date: Optional[datetime] = None
    version: int = 1
    views_count: int = 0
    downloads_count: int = 0
    is_featured: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.meeting_participants is None:
            self.meeting_participants = []
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['document_type'] = self.document_type.value
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Cria instância a partir de dicionário"""
        data['document_type'] = DocumentType(data['document_type'])
        data['status'] = DocumentStatus(data['status'])
        data['priority'] = DocumentPriority(data['priority'])
        return cls(**data)
    
    def increment_view(self):
        """Incrementa contador de visualizações"""
        self.views_count += 1
        self.updated_at = datetime.now()
    
    def increment_download(self):
        """Incrementa contador de downloads"""
        self.downloads_count += 1
        self.updated_at = datetime.now()
    
    def is_expired(self) -> bool:
        """Verifica se o documento expirou"""
        if self.expiration_date is None:
            return False
        return datetime.now() > self.expiration_date
    
    def get_status_badge_color(self) -> str:
        """Retorna cor do badge de status"""
        colors = {
            DocumentStatus.DRAFT: "bg-gray-100 text-gray-800",
            DocumentStatus.PUBLISHED: "bg-green-100 text-green-800",
            DocumentStatus.ARCHIVED: "bg-yellow-100 text-yellow-800",
            DocumentStatus.EXPIRED: "bg-red-100 text-red-800"
        }
        return colors.get(self.status, "bg-gray-100 text-gray-800")
    
    def get_priority_badge_color(self) -> str:
        """Retorna cor do badge de prioridade"""
        colors = {
            DocumentPriority.LOW: "bg-blue-100 text-blue-800",
            DocumentPriority.MEDIUM: "bg-yellow-100 text-yellow-800",
            DocumentPriority.HIGH: "bg-orange-100 text-orange-800",
            DocumentPriority.CRITICAL: "bg-red-100 text-red-800"
        }
        return colors.get(self.priority, "bg-gray-100 text-gray-800") 