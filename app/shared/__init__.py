"""
Utilitários Compartilhados
==========================

Funções e classes utilitárias compartilhadas entre todos os módulos.
"""

from .decorators import admin_required, login_required
from .exceptions import NotFoundError, ValidationError
from .utils import format_date, generate_id, validate_email

__all__ = [
    "format_date",
    "validate_email",
    "generate_id",
    "login_required",
    "admin_required",
    "ValidationError",
    "NotFoundError",
]
