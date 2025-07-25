"""
Shared utilities for Wiki Veloz
"""

import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = {"pdf", "doc", "docx", "txt", "jpg", "jpeg", "png", "gif"}

    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def generate_unique_filename(original_filename):
    """Generate unique filename for upload"""
    ext = original_filename.rsplit(".", 1)[1].lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}"


def save_uploaded_file(file, upload_folder, filename=None):
    """Save uploaded file to disk"""
    if filename is None:
        filename = generate_unique_filename(file.filename)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filename


def format_datetime(dt, format_str="%d/%m/%Y %H:%M"):
    """Format datetime object to string"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
    return dt.strftime(format_str)


def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"


def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)


def get_file_extension(filename):
    """Get file extension from filename"""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    return secure_filename(filename)


def generate_id(prefix="item"):
    """Generate unique ID with prefix"""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def is_valid_email(email):
    """Basic email validation"""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
