"""
Backup Service for Wiki Veloz
CDD v2.0 - Complete backup system with Google Drive integration
"""

import json
import os
import shutil
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from cryptography.fernet import Fernet
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.shared.exceptions import BackupError
from app.core.config import Config


class BackupService:
    """Complete backup service with encryption and Google Drive integration"""
    
    def __init__(self, config: Config):
        self.config = config
        self.backup_folder = Path("backups")
        self.backup_folder.mkdir(exist_ok=True)
        self.backups_info_file = self.backup_folder / "backups_info.json"
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        self.google_drive_service = None
        self._load_backups_info()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = Path("backup_key.key")
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            return key
    
    def _load_backups_info(self):
        """Load backups information"""
        if self.backups_info_file.exists():
            with open(self.backups_info_file, 'r', encoding='utf-8') as f:
                self.backups_info = json.load(f)
        else:
            self.backups_info = []
    
    def _save_backups_info(self):
        """Save backups information"""
        with open(self.backups_info_file, 'w', encoding='utf-8') as f:
            json.dump(self.backups_info, f, indent=2, ensure_ascii=False)
    
    def create_backup(self, description: str = "") -> Dict[str, Any]:
        """Create a complete backup of the system"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"backup_{timestamp}"
            backup_name = f"wiki_veloz_backup_{timestamp}"
            
            # Create temporary directory for backup
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Backup data files
                data_backup_path = temp_path / "data"
                data_backup_path.mkdir()
                
                # Copy all JSON files from data folder
                data_folder = Path(self.config.DATA_FOLDER)
                if data_folder.exists():
                    for json_file in data_folder.glob("*.json"):
                        shutil.copy2(json_file, data_backup_path)
                
                # Backup static files (uploads)
                static_backup_path = temp_path / "static"
                static_backup_path.mkdir()
                
                static_folder = Path("app/static/uploads")
                if static_folder.exists():
                    shutil.copytree(
                        static_folder, 
                        static_backup_path / "uploads", 
                        dirs_exist_ok=True
                    )
                
                # Create backup manifest
                manifest = {
                    "backup_id": backup_id,
                    "backup_name": backup_name,
                    "created_at": datetime.now().isoformat(),
                    "description": description,
                    "version": "1.0",
                    "files": {
                        "data": [f.name for f in data_backup_path.glob("*.json")],
                        "static": [
                        str(f.relative_to(static_backup_path))
                        for f in static_backup_path.rglob("*")
                        if f.is_file()
                    ]
                    }
                }
                
                with open(temp_path / "manifest.json", 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
                
                # Create ZIP file
                zip_filename = f"{backup_name}.zip"
                zip_path = self.backup_folder / zip_filename
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in temp_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(temp_path)
                            zipf.write(file_path, arcname)
                
                # Encrypt the backup
                encrypted_filename = f"{backup_name}.zip.encrypted"
                encrypted_path = self.backup_folder / encrypted_filename
                
                with open(zip_path, 'rb') as f:
                    encrypted_data = self.cipher.encrypt(f.read())
                
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # Get file size
                file_size = encrypted_path.stat().st_size
                
                # Create backup info
                backup_info = {
                    "id": backup_id,
                    "name": backup_name,
                    "filename": encrypted_filename,
                    "size": file_size,
                    "created_at": datetime.now().isoformat(),
                    "description": description,
                    "encrypted": True,
                    "compressed": True,
                    "google_drive_id": None,
                    "status": "completed"
                }
                
                # Add to backups list
                self.backups_info.append(backup_info)
                self._save_backups_info()
                
                # Upload to Google Drive if configured
                if self.google_drive_service:
                    try:
                        drive_id = self._upload_to_google_drive(encrypted_path, backup_name)
                        backup_info["google_drive_id"] = drive_id
                        self._save_backups_info()
                    except Exception as e:
                        print(f"Warning: Failed to upload to Google Drive: {e}")
                
                # Clean up unencrypted file
                zip_path.unlink()
                
                return backup_info
                
        except Exception as e:
            raise BackupError(f"Failed to create backup: {str(e)}")
    
    def get_backups_list(self) -> List[Dict[str, Any]]:
        """Get list of all backups"""
        return self.backups_info
    
    def get_backup_by_id(self, backup_id: str) -> Optional[Dict[str, Any]]:
        """Get backup by ID"""
        return next((b for b in self.backups_info if b.get('id') == backup_id), None)
    
    def restore_backup(self, backup_id: str) -> Dict[str, Any]:
        """Restore a backup"""
        try:
            backup_info = self.get_backup_by_id(backup_id)
            if not backup_info:
                raise BackupError(f"Backup {backup_id} not found")
            
            encrypted_path = self.backup_folder / backup_info['filename']
            if not encrypted_path.exists():
                raise BackupError(f"Backup file not found: {backup_info['filename']}")
            
            # Decrypt the backup
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Create temporary file for decrypted data
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_file.write(decrypted_data)
                temp_zip_path = temp_file.name
            
            try:
                # Extract backup
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    
                    with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
                        zipf.extractall(temp_path)
                    
                    # Read manifest
                    manifest_path = temp_path / "manifest.json"
                    if not manifest_path.exists():
                        raise BackupError("Backup manifest not found")
                    
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    
                    # Restore data files
                    data_backup_path = temp_path / "data"
                    if data_backup_path.exists():
                        data_folder = Path(self.config.DATA_FOLDER)
                        data_folder.mkdir(exist_ok=True)
                        
                        for json_file in data_backup_path.glob("*.json"):
                            shutil.copy2(json_file, data_folder)
                    
                    # Restore static files
                    static_backup_path = temp_path / "static"
                    if static_backup_path.exists():
                        static_folder = Path("app/static/uploads")
                        static_folder.mkdir(parents=True, exist_ok=True)
                        
                        uploads_backup = static_backup_path / "uploads"
                        if uploads_backup.exists():
                            shutil.rmtree(static_folder, ignore_errors=True)
                            shutil.copytree(uploads_backup, static_folder)
                
                return {
                    "success": True,
                    "backup_info": backup_info,
                    "manifest": manifest
                }
                
            finally:
                # Clean up temporary file
                os.unlink(temp_zip_path)
                
        except Exception as e:
            raise BackupError(f"Failed to restore backup: {str(e)}")
    
    def delete_backup(self, backup_id: str) -> Dict[str, Any]:
        """Delete a backup"""
        try:
            backup_info = self.get_backup_by_id(backup_id)
            if not backup_info:
                raise BackupError(f"Backup {backup_id} not found")
            
            # Delete local file
            file_path = self.backup_folder / backup_info['filename']
            if file_path.exists():
                file_path.unlink()
            
            # Delete from Google Drive if exists
            if backup_info.get('google_drive_id') and self.google_drive_service:
                try:
                    self.google_drive_service.files().delete(
                        fileId=backup_info['google_drive_id']
                    ).execute()
                except Exception as e:
                    print(f"Warning: Failed to delete from Google Drive: {e}")
            
            # Remove from list
            self.backups_info = [b for b in self.backups_info if b.get('id') != backup_id]
            self._save_backups_info()
            
            return {"success": True, "message": "Backup deleted successfully"}
            
        except Exception as e:
            raise BackupError(f"Failed to delete backup: {str(e)}")
    
    def get_backup_stats(self) -> Dict[str, Any]:
        """Get backup statistics"""
        total_backups = len(self.backups_info)
        total_size = sum(b.get('size', 0) for b in self.backups_info)
        encrypted_backups = len([b for b in self.backups_info if b.get('encrypted')])
        google_drive_backups = len([b for b in self.backups_info if b.get('google_drive_id')])
        
        return {
            "total_backups": total_backups,
            "total_size": total_size,
            "encrypted_backups": encrypted_backups,
            "google_drive_backups": google_drive_backups,
            "latest_backup": max(self.backups_info, key=lambda x: x.get('created_at', '')) if self.backups_info else None
        }
    
    def setup_google_drive(self, credentials_file: str) -> bool:
        """Setup Google Drive integration"""
        try:
            # Google Drive API scopes
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            creds = None
            
            # Load credentials from file
            if os.path.exists(credentials_file):
                with open(credentials_file, 'r') as f:
                    creds_data = json.load(f)
                
                # Create credentials object
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(credentials_file, 'w') as token:
                    token.write(creds.to_json())
            
            # Build the service
            self.google_drive_service = build('drive', 'v3', credentials=creds)
            
            # Test the connection
            about = self.google_drive_service.about().get(fields="user").execute()
            print(f"Connected to Google Drive as: {about['user']['emailAddress']}")
            
            return True
            
        except Exception as e:
            raise BackupError(f"Failed to setup Google Drive: {str(e)}")
    
    def _upload_to_google_drive(self, file_path: Path, backup_name: str) -> str:
        """Upload file to Google Drive"""
        if not self.google_drive_service:
            raise BackupError("Google Drive not configured")
        
        file_metadata = {
            'name': f"{backup_name}.zip.encrypted",
            'parents': ['root']  # Upload to root folder
        }
        
        media = MediaFileUpload(str(file_path), resumable=True)
        
        file = self.google_drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')
    
    def download_backup(self, backup_id: str) -> bytes:
        """Download backup file"""
        backup_info = self.get_backup_by_id(backup_id)
        if not backup_info:
            raise BackupError(f"Backup {backup_id} not found")
        
        file_path = self.backup_folder / backup_info['filename']
        if not file_path.exists():
            raise BackupError(f"Backup file not found: {backup_info['filename']}")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def cleanup_old_backups(self, max_backups: int = 10) -> int:
        """Clean up old backups, keeping only the most recent ones"""
        if len(self.backups_info) <= max_backups:
            return 0
        
        # Sort by creation date (oldest first)
        sorted_backups = sorted(self.backups_info, key=lambda x: x.get('created_at', ''))
        
        # Remove oldest backups
        backups_to_remove = sorted_backups[:-max_backups]
        
        for backup in backups_to_remove:
            self.delete_backup(backup['id'])
        
        return len(backups_to_remove) 