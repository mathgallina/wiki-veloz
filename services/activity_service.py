"""
Activity service for Wiki Veloz
CDD v2.0 - Activity logging service
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class ActivityService:
    """Service for managing user activities"""
    
    def __init__(self):
        self.log_file = "app/data/activity_log.json"
        self.max_logs = 1000  # Manter apenas os últimos 1000 logs
    
    def log_activity(
        self, 
        user_id: str, 
        action: str, 
        details: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> bool:
        """
        Log a user activity
        
        Args:
            user_id: ID do usuário
            action: Tipo da ação
            details: Detalhes da ação
            ip_address: Endereço IP do usuário
            
        Returns:
            bool: True se logado com sucesso
        """
        try:
            log_entry = {
                "user_id": user_id,
                "action": action,
                "details": details,
                "timestamp": datetime.now().isoformat(),
                "ip_address": ip_address or "unknown",
            }
            
            # Carregar logs existentes
            logs = self._load_logs()
            
            # Adicionar novo log
            logs.append(log_entry)
            
            # Manter apenas os últimos logs
            if len(logs) > self.max_logs:
                logs = logs[-self.max_logs:]
            
            # Salvar logs
            self._save_logs(logs)
            
            return True
            
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_activities(
        self, 
        limit: Optional[int] = None,
        user_id: Optional[str] = None,
        action: Optional[str] = None
    ) -> List[Dict]:
        """
        Get activities with optional filtering
        
        Args:
            limit: Número máximo de atividades
            user_id: Filtrar por usuário
            action: Filtrar por ação
            
        Returns:
            List[Dict]: Lista de atividades
        """
        try:
            logs = self._load_logs()
            
            # Filtrar por usuário se especificado
            if user_id:
                logs = [log for log in logs if log.get("user_id") == user_id]
            
            # Filtrar por ação se especificado
            if action:
                logs = [log for log in logs if log.get("action") == action]
            
            # Ordenar por timestamp (mais recente primeiro)
            logs.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Limitar resultados se especificado
            if limit:
                logs = logs[:limit]
            
            return logs
            
        except Exception as e:
            print(f"Error getting activities: {e}")
            return []
    
    def get_activity_stats(self) -> Dict:
        """
        Get activity statistics
        
        Returns:
            Dict: Estatísticas de atividades
        """
        try:
            logs = self._load_logs()
            
            # Contar por tipo de ação
            action_counts = {}
            user_counts = {}
            
            for log in logs:
                action = log.get("action", "unknown")
                user_id = log.get("user_id", "unknown")
                
                action_counts[action] = action_counts.get(action, 0) + 1
                user_counts[user_id] = user_counts.get(user_id, 0) + 1
            
            return {
                "total_activities": len(logs),
                "action_counts": action_counts,
                "user_counts": user_counts,
                "unique_users": len(user_counts),
                "unique_actions": len(action_counts)
            }
            
        except Exception as e:
            print(f"Error getting activity stats: {e}")
            return {}
    
    def _load_logs(self) -> List[Dict]:
        """Load logs from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading logs: {e}")
            return []
    
    def _save_logs(self, logs: List[Dict]) -> bool:
        """Save logs to file"""
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving logs: {e}")
            return False 