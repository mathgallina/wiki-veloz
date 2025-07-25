"""
Backup Validators for Wiki Veloz
CDD v2.0 - Validation for backup operations
"""

from datetime import datetime
from typing import Any, Dict

from app.shared.exceptions import BackupError


class BackupValidator:
    """Validator for backup operations"""
    
    @staticmethod
    def validate_backup_creation(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate backup creation data"""
        if not isinstance(data, dict):
            raise BackupError("Invalid data format")
        
        description = data.get("description", "")
        if description and not isinstance(description, str):
            raise BackupError("Description must be a string")
        
        if len(description) > 500:
            raise BackupError("Description too long (max 500 characters)")
        
        return {
            "description": description.strip()
        }
    
    @staticmethod
    def validate_backup_id(backup_id: str) -> str:
        """Validate backup ID"""
        if not backup_id:
            raise BackupError("Backup ID is required")
        
        if not isinstance(backup_id, str):
            raise BackupError("Backup ID must be a string")
        
        if len(backup_id) > 100:
            raise BackupError("Backup ID too long")
        
        return backup_id.strip()
    
    @staticmethod
    def validate_backup_config(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate backup configuration"""
        if not isinstance(data, dict):
            raise BackupError("Invalid configuration format")
        
        config = {}
        
        # Auto backup
        auto_backup = data.get("auto_backup")
        if auto_backup is not None:
            if not isinstance(auto_backup, bool):
                raise BackupError("auto_backup must be a boolean")
            config["auto_backup"] = auto_backup
        
        # Backup interval
        backup_interval = data.get("backup_interval_hours")
        if backup_interval is not None:
            if not isinstance(backup_interval, int):
                raise BackupError("backup_interval_hours must be an integer")
            if backup_interval < 1 or backup_interval > 168:  # Max 1 week
                raise BackupError("backup_interval_hours must be between 1 and 168")
            config["backup_interval_hours"] = backup_interval
        
        # Max backups
        max_backups = data.get("max_backups")
        if max_backups is not None:
            if not isinstance(max_backups, int):
                raise BackupError("max_backups must be an integer")
            if max_backups < 1 or max_backups > 100:
                raise BackupError("max_backups must be between 1 and 100")
            config["max_backups"] = max_backups
        
        # Retention days
        retention_days = data.get("backup_retention_days")
        if retention_days is not None:
            if not isinstance(retention_days, int):
                raise BackupError("backup_retention_days must be an integer")
            if retention_days < 1 or retention_days > 365:
                raise BackupError("backup_retention_days must be between 1 and 365")
            config["backup_retention_days"] = retention_days
        
        # Encrypt backups
        encrypt_backups = data.get("encrypt_backups")
        if encrypt_backups is not None:
            if not isinstance(encrypt_backups, bool):
                raise BackupError("encrypt_backups must be a boolean")
            config["encrypt_backups"] = encrypt_backups
        
        # Include logs
        include_logs = data.get("include_logs")
        if include_logs is not None:
            if not isinstance(include_logs, bool):
                raise BackupError("include_logs must be a boolean")
            config["include_logs"] = include_logs
        
        # Include uploads
        include_uploads = data.get("include_uploads")
        if include_uploads is not None:
            if not isinstance(include_uploads, bool):
                raise BackupError("include_uploads must be a boolean")
            config["include_uploads"] = include_uploads
        
        return config
    
    @staticmethod
    def validate_google_drive_setup(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Google Drive setup data"""
        if not isinstance(data, dict):
            raise BackupError("Invalid data format")
        
        credentials_file = data.get("credentials_file")
        if not credentials_file:
            raise BackupError("credentials_file is required")
        
        if not isinstance(credentials_file, str):
            raise BackupError("credentials_file must be a string")
        
        return {
            "credentials_file": credentials_file.strip()
        }
    
    @staticmethod
    def validate_backup_restore(backup_id: str, confirm: bool = False) -> Dict[str, Any]:
        """Validate backup restoration"""
        if not confirm:
            raise BackupError("Backup restoration requires confirmation")
        
        return {
            "backup_id": BackupValidator.validate_backup_id(backup_id),
            "confirmed": True
        }
    
    @staticmethod
    def validate_backup_deletion(backup_id: str, confirm: bool = False) -> Dict[str, Any]:
        """Validate backup deletion"""
        if not confirm:
            raise BackupError("Backup deletion requires confirmation")
        
        return {
            "backup_id": BackupValidator.validate_backup_id(backup_id),
            "confirmed": True
        }
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Dict[str, datetime]:
        """Validate date range for backup queries"""
        try:
            start = datetime.fromisoformat(start_date)
        except ValueError:
            raise BackupError("Invalid start_date format")
        
        try:
            end = datetime.fromisoformat(end_date)
        except ValueError:
            raise BackupError("Invalid end_date format")
        
        if start > end:
            raise BackupError("start_date must be before end_date")
        
        return {
            "start_date": start,
            "end_date": end
        } 