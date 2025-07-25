"""
Backup Repository for Wiki Veloz
CDD v2.0 - Data access layer for backup system
"""

import json
from typing import List, Optional
from pathlib import Path

from app.modules.backup.models.backup import Backup, BackupStats, BackupConfig
from app.shared.exceptions import BackupError


class BackupRepository:
    """Repository for backup data access"""
    
    def __init__(self, backup_folder: str = "backups"):
        self.backup_folder = Path(backup_folder)
        self.backup_folder.mkdir(exist_ok=True)
        self.backups_info_file = self.backup_folder / "backups_info.json"
        self.config_file = self.backup_folder / "backup_config.json"
    
    def get_all_backups(self) -> List[Backup]:
        """Get all backups"""
        try:
            if not self.backups_info_file.exists():
                return []
            
            with open(self.backups_info_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return [Backup.from_dict(backup_data) for backup_data in data]
            
        except Exception as e:
            raise BackupError(f"Failed to load backups: {str(e)}")
    
    def get_backup_by_id(self, backup_id: str) -> Optional[Backup]:
        """Get backup by ID"""
        backups = self.get_all_backups()
        return next((b for b in backups if b.id == backup_id), None)
    
    def save_backup(self, backup: Backup) -> bool:
        """Save backup to repository"""
        try:
            backups = self.get_all_backups()
            
            # Update existing or add new
            existing_index = next(
                (i for i, b in enumerate(backups) if b.id == backup.id), 
                None
            )
            
            if existing_index is not None:
                backups[existing_index] = backup
            else:
                backups.append(backup)
            
            # Save to file
            with open(self.backups_info_file, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in backups], f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            raise BackupError(f"Failed to save backup: {str(e)}")
    
    def delete_backup(self, backup_id: str) -> bool:
        """Delete backup from repository"""
        try:
            backups = self.get_all_backups()
            backups = [b for b in backups if b.id != backup_id]
            
            with open(self.backups_info_file, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in backups], f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            raise BackupError(f"Failed to delete backup: {str(e)}")
    
    def get_backup_stats(self) -> BackupStats:
        """Get backup statistics"""
        try:
            backups = self.get_all_backups()
            
            total_backups = len(backups)
            total_size = sum(b.size for b in backups)
            encrypted_backups = len([b for b in backups if b.encrypted])
            google_drive_backups = len([b for b in backups if b.google_drive_id])
            
            latest_backup = None
            if backups:
                latest_backup = max(backups, key=lambda x: x.created_date)
            
            return BackupStats(
                total_backups=total_backups,
                total_size=total_size,
                encrypted_backups=encrypted_backups,
                google_drive_backups=google_drive_backups,
                latest_backup=latest_backup
            )
            
        except Exception as e:
            raise BackupError(f"Failed to get backup stats: {str(e)}")
    
    def get_config(self) -> BackupConfig:
        """Get backup configuration"""
        try:
            if not self.config_file.exists():
                return BackupConfig()
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return BackupConfig.from_dict(data)
            
        except Exception as e:
            raise BackupError(f"Failed to load backup config: {str(e)}")
    
    def save_config(self, config: BackupConfig) -> bool:
        """Save backup configuration"""
        try:
            if not config.validate():
                raise BackupError("Invalid backup configuration")
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            raise BackupError(f"Failed to save backup config: {str(e)}")
    
    def cleanup_old_backups(self, max_backups: int) -> int:
        """Clean up old backups"""
        try:
            backups = self.get_all_backups()
            
            if len(backups) <= max_backups:
                return 0
            
            # Sort by creation date (oldest first)
            sorted_backups = sorted(backups, key=lambda x: x.created_date)
            
            # Remove oldest backups
            backups_to_remove = sorted_backups[:-max_backups]
            
            for backup in backups_to_remove:
                # Delete file
                backup_file = self.backup_folder / backup.filename
                if backup_file.exists():
                    backup_file.unlink()
                
                # Remove from repository
                self.delete_backup(backup.id)
            
            return len(backups_to_remove)
            
        except Exception as e:
            raise BackupError(f"Failed to cleanup old backups: {str(e)}")
    
    def backup_exists(self, backup_id: str) -> bool:
        """Check if backup exists"""
        return self.get_backup_by_id(backup_id) is not None
    
    def get_backup_file_path(self, backup_id: str) -> Optional[Path]:
        """Get backup file path"""
        backup = self.get_backup_by_id(backup_id)
        if not backup:
            return None
        
        file_path = self.backup_folder / backup.filename
        return file_path if file_path.exists() else None
    
    def get_backups_by_status(self, status: str) -> List[Backup]:
        """Get backups by status"""
        backups = self.get_all_backups()
        return [b for b in backups if b.status == status]
    
    def get_backups_by_date_range(self, start_date, end_date) -> List[Backup]:
        """Get backups by date range"""
        backups = self.get_all_backups()
        return [
            b for b in backups 
            if start_date <= b.created_date <= end_date
        ] 