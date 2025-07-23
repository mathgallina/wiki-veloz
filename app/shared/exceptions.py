"""
Exceções Customizadas
=====================

Exceções customizadas compartilhadas entre módulos.
"""


class ValidationError(Exception):
    """Exceção para errors de validação."""

    def __init__(self, message: str, field: str = None):
        """
        Inicializa a exceção.

        Args:
            message (str): Mensagem de error
            field (str): Campo que causou o error
        """
        self.message = message
        self.field = field
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exceção para recursos não encontrados."""

    def __init__(self, resource: str, resource_id: str = None):
        """
        Inicializa a exceção.

        Args:
            resource (str): Tipo de recurso
            resource_id (str): ID do recurso não encontrado
        """
        self.resource = resource
        self.resource_id = resource_id
        self.message = f"{resource} não encontrado"
        if resource_id:
            self.message += f": {resource_id}"
        super().__init__(self.message)
