"""
Utilitários Básicos
===================

Funções utilitárias básicas compartilhadas entre módulos.
"""

import re
import uuid
from datetime import datetime


def format_date(date_string: str, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formata uma data string para exibição.

    Args:
        date_string (str): Data em formato ISO
        format_str (str): Formato de saída

    Returns:
        str: Data formatada
    """
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime(format_str)
    except (ValueError, AttributeError):
        return date_string


def validate_email(email: str) -> bool:
    """
    Valida formato de email.

    Args:
        email (str): Email a set validado

    Returns:
        bool: True se email válido
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def generate_id(prefix: str = "") -> str:
    """
    Gera ID único.

    Args:
        prefix (str): Prefixo para o ID

    Returns:
        str: ID único gerado
    """
    unique_id = str(uuid.uuid4()).replace("-", "")[:8]
    return f"{prefix}{unique_id}" if prefix else unique_id
