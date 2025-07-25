"""
Custom exceptions for Wiki Veloz
"""


class WikiVelozError(Exception):
    """Base exception for Wiki Veloz"""

    pass


class AuthenticationError(WikiVelozError):
    """Authentication related errors"""

    pass


class AuthorizationError(WikiVelozError):
    """Authorization related errors"""

    pass


class ValidationError(WikiVelozError):
    """Validation related errors"""

    pass


class FileUploadError(WikiVelozError):
    """File upload related errors"""

    pass


class DatabaseError(WikiVelozError):
    """Database related errors"""

    pass


class BackupError(WikiVelozError):
    """Backup related errors"""

    pass


class NotificationError(WikiVelozError):
    """Notification related errors"""

    pass


class PDFProcessingError(WikiVelozError):
    """PDF processing related errors"""

    pass


class GoogleDriveError(WikiVelozError):
    """Google Drive related errors"""

    pass


class AnalyticsError(WikiVelozError):
    """Analytics related errors"""

    pass
