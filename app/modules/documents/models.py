"""
Modelos de dados para Documentos Corporations
"""
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DocumentType(Enum):
    """Tipos de documentos corporations"""

    ATA = "ata"  # Ata de reunião
    REGULAMENTO = "regulamento"  # Regulamento
    POLITICA = "politica"  # Política
    PROCEDIMENTO = "procedimento"  # Procedimento
    MANUAL = "manual"  # Manual
    OUTRO = "outro"  # Outros


class DocumentStatus(Enum):
    """Status dos documentos"""

    ATIVO = "ativo"  # Ativo
    RASCUNHO = "rascunho"  # Rascunho
    ARQUIVADO = "arquivado"  # Arquivado


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
    icon: str
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
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
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Document:
    """Modelo principal de documento corporation"""

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

    def to_dict(self) -> dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)


class DocumentAttachmentType(Enum):
    """Tipos de anexos permitidos"""

    PDF = "pdf"
    IMAGE = "image"
    DOCUMENT = "document"


@dataclass
class DocumentAttachment:
    """Anexo de documento"""

    id: str
    document_id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str
    mime_type: str
    description: str
    uploaded_by: str
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def get_file_extension(self) -> str:
        """Retorna a extensão do arquivo"""
        return (
            self.original_filename.split(".")[-1].lower()
            if "." in self.original_filename
            else ""
        )

    def is_image(self) -> bool:
        """Verifica se é uma imagem"""
        return self.mime_type.startswith("image/")

    def is_pdf(self) -> bool:
        """Verifica se é um PDF"""
        return self.mime_type == "application/pdf"

    def get_file_size_mb(self) -> float:
        """Retorna o tamanho em MB"""
        return round(self.file_size / (1024 * 1024), 2)

    def get_icon_class(self) -> str:
        """Retorna a classe do ícone baseada no tipo de arquivo"""
        if self.is_pdf():
            return "fas fa-file-pdf"
        elif self.is_image():
            return "fas fa-file-image"
        else:
            return "fas fa-file"
