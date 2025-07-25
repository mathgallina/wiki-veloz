"""
Shared utilities and components for Wiki Veloz
"""

from .decorators import (
    admin_required,
    api_response,
    handle_errors,
    log_activity,
    validate_json,
)
from .exceptions import (
    AnalyticsError,
    AuthenticationError,
    AuthorizationError,
    BackupError,
    DatabaseError,
    FileUploadError,
    GoogleDriveError,
    NotificationError,
    PDFProcessingError,
    ValidationError,
    WikiVelozError,
)
from .utils import (
    allowed_file,
    create_directory_if_not_exists,
    format_datetime,
    format_file_size,
    generate_id,
    generate_unique_filename,
    get_file_extension,
    is_valid_email,
    sanitize_filename,
    save_uploaded_file,
)

__all__ = [
    # Decorators
    "admin_required",
    "api_response",
    "validate_json",
    "log_activity",
    "handle_errors",
    # Exceptions
    "WikiVelozError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "FileUploadError",
    "DatabaseError",
    "BackupError",
    "NotificationError",
    "PDFProcessingError",
    "GoogleDriveError",
    "AnalyticsError",
    # Utils
    "allowed_file",
    "generate_unique_filename",
    "save_uploaded_file",
    "format_datetime",
    "format_file_size",
    "create_directory_if_not_exists",
    "get_file_extension",
    "sanitize_filename",
    "generate_id",
    "is_valid_email",
]
