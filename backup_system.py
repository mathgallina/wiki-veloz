"""
Sistema de Backup e Restauração - Wiki Veloz Fibra
==================================================

Este módulo fornece funcionalidades completas de backup e restauração
com suporte ao Google Drive, compressão e criptografia.
"""

import json
import logging
import shutil
import tempfile
import threading
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Google Drive API
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print(
        "⚠️ Google Drive API não disponível. "
        "Install: pip install google-auth google-auth-oauthlib "
        "google-auth-httplib2 google-api-python-client"
    )

# Criptografia
try:
    from cryptography.fernet import Fernet

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("⚠️ Criptografia não disponível. Install: pip install cryptography")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("backup.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class BackupSystem:
    """Sistema principal de backup e restauração"""

    def __init__(self, data_dir: str = "data", backup_dir: str = "backups"):
        self.data_dir = Path(data_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

        # Configurações
        self.encryption_key = None
        self.google_drive_service = None
        self.backup_folder_id = None

        # Carregar configurações
        self.load_config()

        # Inicializar criptografia se disponível
        if CRYPTOGRAPHY_AVAILABLE:
            self.setup_encryption()

    def load_config(self):
        """Carrega configurações do backup"""
        config_file = Path("backup_config.json")
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                logger.error(f"Error ao carregar configuração: {e}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()

    def get_default_config(self) -> dict:
        """Retorna configuração padrão"""
        return {
            "auto_backup": True,
            "backup_interval_hours": 24,
            "max_backups": 30,
            "encrypt_backups": True,
            "use_google_drive": False,
            "google_drive_folder": "Wiki-Veloz-Backups",
            "backup_retention_days": 90,
            "include_logs": True,
            "include_uploads": True,
            "compression_level": 6,
        }

    def save_config(self):
        """Salva configurações"""
        try:
            with open("backup_config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error ao salvar configuração: {e}")

    def setup_encryption(self):
        """Configura criptografia"""
        if not CRYPTOGRAPHY_AVAILABLE:
            return

        key_file = Path("backup_key.key")
        if key_file.exists():
            try:
                with open(key_file, "rb") as f:
                    self.encryption_key = f.read()
            except Exception as e:
                logger.error(f"Error ao carregar chave de criptografia: {e}")
                self.generate_encryption_key()
        else:
            self.generate_encryption_key()

    def generate_encryption_key(self):
        """Gera nova chave de criptografia"""
        if not CRYPTOGRAPHY_AVAILABLE:
            return

        try:
            self.encryption_key = Fernet.generate_key()
            with open("backup_key.key", "wb") as f:
                f.write(self.encryption_key)
            logger.info("✅ Nova chave de criptografia gerada")
        except Exception as e:
            logger.error(f"Error ao gerar chave de criptografia: {e}")

    def encrypt_file(self, file_path: Path) -> Path:
        """Criptografa um arquivo"""
        if not CRYPTOGRAPHY_AVAILABLE or not self.encryption_key:
            return file_path

        try:
            fernet = Fernet(self.encryption_key)
            encrypted_path = file_path.with_suffix(file_path.suffix + ".encrypted")

            with open(file_path, "rb") as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)

            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)

            return encrypted_path
        except Exception as e:
            logger.error(f"Error ao criptografar arquivo: {e}")
            return file_path

    def decrypt_file(self, file_path: Path) -> Path:
        """Descriptografa um arquivo"""
        if not CRYPTOGRAPHY_AVAILABLE or not self.encryption_key:
            return file_path

        try:
            fernet = Fernet(self.encryption_key)
            decrypted_path = file_path.with_suffix("").with_suffix(
                file_path.suffix.replace(".encrypted", "")
            )

            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            with open(decrypted_path, "wb") as f:
                f.write(decrypted_data)

            return decrypted_path
        except Exception as e:
            logger.error(f"Error ao descriptografar arquivo: {e}")
            return file_path

    def create_backup(self, description: str = "") -> dict:
        """Cria um novo backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"wiki_veloz_backup_{timestamp}"
            backup_path = self.backup_dir / f"{backup_name}.zip"

            # Criar backup temporário
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_backup_path = Path(temp_dir) / f"{backup_name}.zip"

                # Criar arquivo ZIP
                with zipfile.ZipFile(
                    temp_backup_path,
                    "w",
                    zipfile.ZIP_DEFLATED,
                    compresslevel=self.config["compression_level"],
                ) as zipf:
                    # Adicionar arquivos de dados
                    for data_file in self.data_dir.glob("*.json"):
                        zipf.write(data_file, f"data/{data_file.name}")

                    # Adicionar logs se configurado
                    if self.config["include_logs"]:
                        log_files = ["backup.log", "app.log"]
                        for log_file in log_files:
                            if Path(log_file).exists():
                                zipf.write(log_file, f"logs/{log_file}")

                    # Adicionar uploads se configurado
                    if self.config["include_uploads"]:
                        uploads_dir = Path("static/uploads")
                        if uploads_dir.exists():
                            for upload_file in uploads_dir.rglob("*"):
                                if upload_file.is_file():
                                    zipf.write(
                                        upload_file,
                                        f"uploads/{upload_file.relative_to(uploads_dir)}",
                                    )

                # Mover para diretório de backup
                shutil.move(str(temp_backup_path), str(backup_path))

            # Criptografar se configurado
            if self.config["encrypt_backups"]:
                backup_path = self.encrypt_file(backup_path)

            # Informações do backup
            backup_info = {
                "id": f"backup_{timestamp}",
                "name": backup_name,
                "filename": backup_path.name,
                "size": backup_path.stat().st_size,
                "created_at": datetime.now().isoformat(),
                "description": description,
                "encrypted": self.config["encrypt_backups"],
                "compressed": True,
            }

            # Salvar informações do backup
            self.save_backup_info(backup_info)

            # Upload para Google Drive se configurado
            if self.config["use_google_drive"] and GOOGLE_DRIVE_AVAILABLE:
                self.upload_to_google_drive(backup_path, backup_info)

            # Limpar backups antigos
            self.cleanup_old_backups()

            logger.info(
                f"✅ Backup criado: {backup_path.name} ({backup_info['size']} bytes)"
            )
            return backup_info

        except Exception as e:
            logger.error(f"❌ Error ao criar backup: {e}")
            return {"error": str(e)}

    def save_backup_info(self, backup_info: dict):
        """Salva informações do backup"""
        backups_file = Path("backups/backups_info.json")
        try:
            if backups_file.exists():
                with open(backups_file, encoding="utf-8") as f:
                    backups = json.load(f)
            else:
                backups = []

            backups.append(backup_info)

            with open(backups_file, "w", encoding="utf-8") as f:
                json.dump(backups, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error ao salvar informações do backup: {e}")

    def get_backups_list(self) -> list[dict]:
        """Retorna lista de backups"""
        backups_file = Path("backups/backups_info.json")
        try:
            if backups_file.exists():
                with open(backups_file, encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error ao carregar lista de backups: {e}")
            return []

    def restore_backup(self, backup_id: str) -> dict:
        """Restaura um backup"""
        try:
            backups = self.get_backups_list()
            backup_info = next((b for b in backups if b["id"] == backup_id), None)

            if not backup_info:
                return {"error": "Backup não encontrado"}

            backup_file = self.backup_dir / backup_info["filename"]

            if not backup_file.exists():
                return {"error": "Arquivo de backup não encontrado"}

            # Descriptografar se necessário
            if backup_info.get("encrypted", False):
                backup_file = self.decrypt_file(backup_file)

            # Criar backup do estado atual antes da restauração
            current_backup = self.create_backup(
                "Backup automático antes da restauração"
            )

            # Restaurar dados
            with zipfile.ZipFile(backup_file, "r") as zipf:
                # Restaurar arquivos de dados
                for file_info in zipf.infolist():
                    if file_info.filename.startswith("data/"):
                        zipf.extract(file_info, ".")
                        logger.info(f"Restaurado: {file_info.filename}")

            logger.info(f"✅ Backup restaurado: {backup_info['name']}")
            return {
                "success": True,
                "message": f"Backup '{backup_info['name']}' restaurado com sucesso",
                "backup_info": backup_info,
                "current_backup": current_backup,
            }

        except Exception as e:
            logger.error(f"❌ Error ao restaurar backup: {e}")
            return {"error": str(e)}

    def delete_backup(self, backup_id: str) -> dict:
        """Remove um backup"""
        try:
            backups = self.get_backups_list()
            backup_info = next((b for b in backups if b["id"] == backup_id), None)

            if not backup_info:
                return {"error": "Backup não encontrado"}

            # Remover arquivo
            backup_file = self.backup_dir / backup_info["filename"]
            if backup_file.exists():
                backup_file.unlink()

            # Remover do Google Drive se configurado
            if self.config["use_google_drive"] and GOOGLE_DRIVE_AVAILABLE:
                self.delete_from_google_drive(backup_info.get("google_drive_id"))

            # Remover das informações
            backups = [b for b in backups if b["id"] != backup_id]
            with open("backups/backups_info.json", "w", encoding="utf-8") as f:
                json.dump(backups, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Backup removido: {backup_info['name']}")
            return {"success": True, "message": "Backup removido com sucesso"}

        except Exception as e:
            logger.error(f"❌ Error ao remover backup: {e}")
            return {"error": str(e)}

    def cleanup_old_backups(self):
        """Remove backups antigos baseado na configuração"""
        try:
            backups = self.get_backups_list()
            max_backups = self.config["max_backups"]
            retention_days = self.config["backup_retention_days"]

            # Ordenar por data de criação
            backups.sort(key=lambda x: x["created_at"], reverse=True)

            # Remover backups excedentes
            if len(backups) > max_backups:
                for backup in backups[max_backups:]:
                    self.delete_backup(backup["id"])

            # Remover backups antigos
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            for backup in backups:
                backup_date = datetime.fromisoformat(backup["created_at"])
                if backup_date < cutoff_date:
                    self.delete_backup(backup["id"])

        except Exception as e:
            logger.error(f"Error ao limpar backups antigos: {e}")

    def setup_google_drive(self, credentials_file: str = "credentials.json") -> bool:
        """Configura integração com Google Drive"""
        if not GOOGLE_DRIVE_AVAILABLE:
            logger.error("Google Drive API não disponível")
            return False

        try:
            SCOPES = ["https://www.googleapis.com/auth/drive.file"]

            creds = None
            token_file = Path("token.json")

            if token_file.exists():
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not Path(credentials_file).exists():
                        logger.error(
                            f"Arquivo de credenciais não encontrado: {credentials_file}"
                        )
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                with open(token_file, "w") as token:
                    token.write(creds.to_json())

            self.google_drive_service = build("drive", "v3", credentials=creds)

            # Criar ou encontrar pasta de backup
            self.backup_folder_id = self.get_or_create_backup_folder()

            self.config["use_google_drive"] = True
            self.save_config()

            logger.info("✅ Google Drive configurado com sucesso")
            return True

        except Exception as e:
            logger.error(f"❌ Error ao configurar Google Drive: {e}")
            return False

    def get_or_create_backup_folder(self) -> str:
        """Cria ou encontra a pasta de backup no Google Drive"""
        try:
            # Buscar pasta existente
            results = (
                self.google_drive_service.files()
                .list(
                    q=f"name='{self.config['google_drive_folder']}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                    spaces="drive",
                    fields="files(id, name)",
                )
                .execute()
            )

            if results["files"]:
                return results["files"][0]["id"]

            # Criar nova pasta
            file_metadata = {
                "name": self.config["google_drive_folder"],
                "mimeType": "application/vnd.google-apps.folder",
            }

            folder = (
                self.google_drive_service.files()
                .create(body=file_metadata, fields="id")
                .execute()
            )

            return folder["id"]

        except Exception as e:
            logger.error(f"Error ao criar pasta no Google Drive: {e}")
            return None

    def upload_to_google_drive(self, file_path: Path, backup_info: dict) -> bool:
        """Faz upload do backup para o Google Drive"""
        if not self.google_drive_service or not self.backup_folder_id:
            return False

        try:
            file_metadata = {"name": file_path.name, "parents": [self.backup_folder_id]}

            media = MediaFileUpload(str(file_path), resumable=True)

            file = (
                self.google_drive_service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )

            # Atualizar informações do backup
            backup_info["google_drive_id"] = file["id"]
            self.update_backup_info(backup_info)

            logger.info(f"✅ Backup enviado para Google Drive: {file_path.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Error ao enviar para Google Drive: {e}")
            return False

    def download_from_google_drive(self, file_id: str, destination_path: Path) -> bool:
        """Baixa arquivo do Google Drive"""
        if not self.google_drive_service:
            return False

        try:
            request = self.google_drive_service.files().get_media(fileId=file_id)
            with open(destination_path, "wb") as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()

            return True

        except Exception as e:
            logger.error(f"❌ Error ao baixar do Google Drive: {e}")
            return False

    def delete_from_google_drive(self, file_id: str) -> bool:
        """Remove arquivo do Google Drive"""
        if not self.google_drive_service or not file_id:
            return False

        try:
            self.google_drive_service.files().delete(fileId=file_id).execute()
            logger.info(f"✅ Arquivo removido do Google Drive: {file_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error ao remover do Google Drive: {e}")
            return False

    def update_backup_info(self, backup_info: dict):
        """Atualiza informações de um backup"""
        backups = self.get_backups_list()
        for i, backup in enumerate(backups):
            if backup["id"] == backup_info["id"]:
                backups[i] = backup_info
                break

        with open("backups/backups_info.json", "w", encoding="utf-8") as f:
            json.dump(backups, f, ensure_ascii=False, indent=2)

    def start_auto_backup(self):
        """Inicia backup automático"""
        if not self.config["auto_backup"]:
            return

        def run_backup():
            while True:
                try:
                    self.create_backup("Backup automático")
                    time.sleep(self.config["backup_interval_hours"] * 3600)
                except Exception as e:
                    logger.error(f"Error no backup automático: {e}")
                    time.sleep(3600)  # Esperar 1 hora antes de tentar novamente

        thread = threading.Thread(target=run_backup, daemon=True)
        thread.start()
        logger.info("✅ Backup automático iniciado")

    def get_backup_stats(self) -> dict:
        """Retorna estatísticas dos backups"""
        backups = self.get_backups_list()

        if not backups:
            return {
                "total_backups": 0,
                "total_size": 0,
                "oldest_backup": None,
                "newest_backup": None,
                "encrypted_backups": 0,
                "google_drive_backups": 0,
            }

        total_size = sum(b.get("size", 0) for b in backups)
        encrypted_count = sum(1 for b in backups if b.get("encrypted", False))
        google_drive_count = sum(1 for b in backups if b.get("google_drive_id"))

        dates = [datetime.fromisoformat(b["created_at"]) for b in backups]

        return {
            "total_backups": len(backups),
            "total_size": total_size,
            "oldest_backup": min(dates).isoformat() if dates else None,
            "newest_backup": max(dates).isoformat() if dates else None,
            "encrypted_backups": encrypted_count,
            "google_drive_backups": google_drive_count,
        }


# Instância global do sistema de backup
backup_system = BackupSystem()


def init_backup_system():
    """Inicializa o sistema de backup"""
    try:
        # Criar diretório de backups se não existir
        Path("backups").mkdir(exist_ok=True)

        # Iniciar backup automático se configurado
        if backup_system.config["auto_backup"]:
            backup_system.start_auto_backup()

        logger.info("✅ Sistema de backup inicializado")

    except Exception as e:
        logger.error(f"❌ Error ao inicializar sistema de backup: {e}")


if __name__ == "__main__":
    # Teste do sistema
    init_backup_system()

    # Criar backup de teste
    result = backup_system.create_backup("Backup de teste")
    print(f"Resultado do backup: {result}")

    # Mostrar estatísticas
    stats = backup_system.get_backup_stats()
    print(f"Estatísticas: {stats}")
