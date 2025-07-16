#!/usr/bin/env python3
"""
Sistema de Backup Simplificado - Sem Google Drive
"""

import os
import json
import zipfile
import shutil
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleBackupSystem:
    """Sistema de backup simplificado sem Google Drive"""

    def __init__(self):
        self.backup_dir = "backups"
        self.data_files = [
            "data/users.json",
            "data/pages.json",
            "data/notifications.json",
            "data/activity_log.json"
        ]

        # Criar diretório de backup se não existir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"✅ Diretório de backup criado: {self.backup_dir}")

    def create_backup(self):
        """Cria um backup local simples"""
        try:
            # Nome do arquivo de backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"wiki_veloz_backup_{timestamp}.zip"
            backup_path = os.path.join(self.backup_dir, backup_filename)

            # Criar arquivo ZIP
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Adicionar arquivos de dados
                for data_file in self.data_files:
                    if os.path.exists(data_file):
                        zipf.write(data_file, os.path.basename(data_file))
                        logger.info(f"✅ Adicionado ao backup: {data_file}")
                    else:
                        logger.warning(f"⚠️ Arquivo não encontrado: {data_file}")

                # Adicionar informações do sistema
                system_info = {
                    "backup_date": datetime.now().isoformat(),
                    "version": "1.0",
                    "files_included": [f for f in self.data_files if os.path.exists(f)],
                    "total_files": len([f for f in self.data_files if os.path.exists(f)])
                }

                zipf.writestr("system_info.json", json.dumps(system_info, indent=2))

            # Obter tamanho do arquivo
            file_size = os.path.getsize(backup_path)
            logger.info(f"✅ Backup criado: {backup_filename} ({file_size} bytes)")

            return {
                "success": True,
                "filename": backup_filename,
                "size": file_size,
                "path": backup_path
            }

        except Exception as e:
            logger.error(f"❌ Erro ao criar backup: {e}")
            return {"success": False, "error": str(e)}

    def list_backups(self):
        """Lista todos os backups disponíveis"""
        try:
            backups = []
            if os.path.exists(self.backup_dir):
                for filename in os.listdir(self.backup_dir):
                    if filename.endswith('.zip') and filename.startswith('wiki_veloz_backup_'):
                        file_path = os.path.join(self.backup_dir, filename)
                        file_size = os.path.getsize(file_path)
                        file_date = datetime.fromtimestamp(os.path.getctime(file_path))

                        backups.append({
                            "filename": filename,
                            "size": file_size,
                            "date": file_date.isoformat(),
                            "size_formatted": f"{file_size / 1024:.1f} KB"
                        })

            # Ordenar por data (mais recente primeiro)
            backups.sort(key=lambda x: x["date"], reverse=True)
            return backups

        except Exception as e:
            logger.error(f"❌ Erro ao listar backups: {e}")
            return []

    def get_stats(self):
        """Retorna estatísticas do sistema de backup"""
        backups = self.list_backups()

        total_backups = len(backups)
        total_size = sum(b["size"] for b in backups)

        return {
            "total_backups": total_backups,
            "total_size": total_size,
            "total_size_formatted": f"{total_size / 1024:.1f} KB",
            "google_drive_enabled": False,
            "google_drive_backups": 0
        }

# Instância global
backup_system = SimpleBackupSystem()

if __name__ == "__main__":
    print("🔧 Testando sistema de backup simplificado...")

    # Criar backup
    result = backup_system.create_backup()
    if result["success"]:
        print(f"✅ Backup criado: {result['filename']}")
    else:
        print(f"❌ Erro: {result['error']}")

    # Listar backups
    backups = backup_system.list_backups()
    print(f"📁 Total de backups: {len(backups)}")

    # Estatísticas
    stats = backup_system.get_stats()
    print(f"📊 Estatísticas: {stats}")
