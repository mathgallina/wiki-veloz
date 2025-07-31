"""
Backup Models for Wiki Veloz
CDD v2.0 - Data models for backup system
"""

from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Backup:
    """Backup model"""
    
    id: str
    name: str
    filename: str
    size: int
    created_at: str
    description: str
    encrypted: bool = True
    compressed: bool = True
    google_drive_id: Optional[str] = None
    status: str = "completed"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Backup':
        """Create from dictionary"""
        return cls(**data)
    
    @property
    def created_date(self) -> datetime:
        """Get created date as datetime object"""
        return datetime.fromisoformat(self.created_at)
    
    @property
    def formatted_size(self) -> str:
        """Get formatted size string"""
        return self._format_bytes(self.size)
    
    @property
    def formatted_date(self) -> str:
        """Get formatted date string"""
        return self.created_date.strftime("%d/%m/%Y %H:%M")
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable string"""
        if bytes_value == 0:
            return "0 Bytes"
        
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        i = 0
        
        while bytes_value >= k and i < len(sizes) - 1:
            bytes_value /= k
            i += 1
        
        return f"{bytes_value:.2f} {sizes[i]}"


@dataclass
class BackupStats:
    """Backup statistics model"""
    
    total_backups: int
    total_size: int
    encrypted_backups: int
    google_drive_backups: int
    latest_backup: Optional[Backup] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        if self.latest_backup:
            data['latest_backup'] = self.latest_backup.to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupStats':
        """Create from dictionary"""
        latest_backup_data = data.pop('latest_backup', None)
        stats = cls(**data)
        if latest_backup_data:
            stats.latest_backup = Backup.from_dict(latest_backup_data)
        return stats
    
    @property
    def formatted_total_size(self) -> str:
        """Get formatted total size"""
        return self._format_bytes(self.total_size)
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable string"""
        if bytes_value == 0:
            return "0 Bytes"
        
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        i = 0
        
        while bytes_value >= k and i < len(sizes) - 1:
            bytes_value /= k
            i += 1
        
        return f"{bytes_value:.2f} {sizes[i]}"


@dataclass
class BackupConfig:
    """Backup configuration model"""
    
    auto_backup: bool = False
    backup_interval_hours: int = 24
    max_backups: int = 10
    backup_retention_days: int = 30
    encrypt_backups: bool = True
    include_logs: bool = True
    include_uploads: bool = True
    google_drive_enabled: bool = False
    google_drive_folder_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupConfig':
        """Create from dictionary"""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate configuration"""
        if self.backup_interval_hours < 1:
            return False
        if self.max_backups < 1:
            return False
        if self.backup_retention_days < 1:
            return False
        return True 