"""
Database management for Wiki Veloz
CDD v2.0 - Centralized data management
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.config import Config


class DatabaseManager:
    """Centralized database management for JSON files"""
    
    def __init__(self, config: Config):
        self.config = config
        self.data_folder = config.DATA_FOLDER
        self._ensure_data_folder()
    
    def _ensure_data_folder(self):
        """Ensure data folder exists"""
        os.makedirs(self.data_folder, exist_ok=True)
    
    def load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        filepath = os.path.join(self.data_folder, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def save_data(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Save data to JSON file"""
        filepath = os.path.join(self.data_folder, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
    
    def get_by_id(self, filename: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Get item by ID from file"""
        data = self.load_data(filename)
        return next((item for item in data if item.get('id') == item_id), None)
    
    def create_item(self, filename: str, item: Dict[str, Any]) -> bool:
        """Create new item in file"""
        data = self.load_data(filename)
        data.append(item)
        return self.save_data(filename, data)
    
    def update_item(self, filename: str, item_id: str, updates: Dict[str, Any]) -> bool:
        """Update item in file"""
        data = self.load_data(filename)
        for item in data:
            if item.get('id') == item_id:
                item.update(updates)
                return self.save_data(filename, data)
        return False
    
    def delete_item(self, filename: str, item_id: str) -> bool:
        """Delete item from file"""
        data = self.load_data(filename)
        data = [item for item in data if item.get('id') != item_id]
        return self.save_data(filename, data)
    
    def backup_data(self, filename: str) -> str:
        """Create backup of data file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{filename.replace('.json', '')}_{timestamp}.json"
        backup_path = os.path.join(self.config.BACKUP_FOLDER, backup_filename)
        
        os.makedirs(self.config.BACKUP_FOLDER, exist_ok=True)
        
        data = self.load_data(filename)
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            return ""
    
    def restore_data(self, filename: str, backup_path: str) -> bool:
        """Restore data from backup"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.save_data(filename, data)
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False


class ActivityLogger:
    """Activity logging system"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.log_file = "activity_log.json"
    
    def log_activity(self, user_id: str, action: str, details: str = None) -> bool:
        """Log user activity"""
        activity = {
            "id": f"activity-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.db_manager.create_item(self.log_file, activity)
    
    def get_user_activities(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user activities"""
        activities = self.db_manager.load_data(self.log_file)
        user_activities = [a for a in activities if a.get('user_id') == user_id]
        return sorted(user_activities, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
    
    def cleanup_old_activities(self, days: int = 30) -> int:
        """Clean up old activities"""
        activities = self.db_manager.load_data(self.log_file)
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        original_count = len(activities)
        activities = [
            a for a in activities 
            if datetime.fromisoformat(a.get('timestamp', '')) > cutoff_date
        ]
        
        self.db_manager.save_data(self.log_file, activities)
        return original_count - len(activities)
