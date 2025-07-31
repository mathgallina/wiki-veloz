"""
Backup Routes for Wiki Veloz
CDD v2.0 - Complete backup API endpoints
"""

from io import BytesIO

from flask import Blueprint, jsonify, render_template, request, send_file
from flask_login import current_user, login_required

from app.core.config import Config
from app.modules.backup.repositories.backup_repository import BackupRepository
from app.modules.backup.services.backup_service import BackupService
from app.modules.backup.validators.backup_validator import BackupValidator
from app.shared.exceptions import BackupError

backup_bp = Blueprint("backup", __name__)

# Initialize services
config = Config()
backup_repository = BackupRepository()
backup_service = BackupService(config)


@backup_bp.route("/")
@login_required
def index():
    """Backup management page"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    return render_template("admin_backup.html")


@backup_bp.route("/api/backup/create", methods=["POST"])
@login_required
def create_backup():
    """Create a new backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        data = request.get_json() or {}
        validated_data = BackupValidator.validate_backup_creation(data)
        
        backup_info = backup_service.create_backup(validated_data["description"])
        
        # Save to repository
        backup = backup_service.get_backup_by_id(backup_info["id"])
        if backup:
            backup_repository.save_backup(backup)
        
        return jsonify({
            "success": True,
            "message": "Backup criado com sucesso",
            "backup": backup_info
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/list")
@login_required
def list_backups():
    """List all backups"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        backups = backup_repository.get_all_backups()
        return jsonify({
            "success": True,
            "backups": [backup.to_dict() for backup in backups]
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/<backup_id>/restore", methods=["POST"])
@login_required
def restore_backup(backup_id):
    """Restore a backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        validated_data = BackupValidator.validate_backup_restore(
            backup_id, 
            confirm=request.json.get("confirm", False)
        )
        
        result = backup_service.restore_backup(validated_data["backup_id"])
        
        return jsonify({
            "success": True,
            "message": "Backup restaurado com sucesso",
            "result": result
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/<backup_id>/delete", methods=["DELETE"])
@login_required
def delete_backup(backup_id):
    """Delete a backup"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        validated_data = BackupValidator.validate_backup_deletion(
            backup_id,
            confirm=request.json.get("confirm", False)
        )
        
        backup_service.delete_backup(validated_data["backup_id"])
        
        return jsonify({
            "success": True,
            "message": "Backup excluído com sucesso"
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/<backup_id>/download")
@login_required
def download_backup(backup_id):
    """Download a backup file"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        BackupValidator.validate_backup_id(backup_id)
        
        backup = backup_repository.get_backup_by_id(backup_id)
        if not backup:
            return jsonify({"error": "Backup não encontrado"}), 404
        
        file_data = backup_service.download_backup(backup_id)
        
        return send_file(
            BytesIO(file_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=backup.filename
        )
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/stats")
@login_required
def get_backup_stats():
    """Get backup statistics"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        stats = backup_repository.get_backup_stats()
        config = backup_repository.get_config()
        
        return jsonify({
            "success": True,
            "stats": stats.to_dict(),
            "config": config.to_dict()
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/config", methods=["GET", "PUT"])
@login_required
def manage_backup_config():
    """Manage backup configuration"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        if request.method == "GET":
            config = backup_repository.get_config()
            return jsonify({
                "success": True,
                "config": config.to_dict()
            })
        
        elif request.method == "PUT":
            data = request.get_json() or {}
            validated_config = BackupValidator.validate_backup_config(data)
            
            current_config = backup_repository.get_config()
            
            # Update configuration
            for key, value in validated_config.items():
                setattr(current_config, key, value)
            
            backup_repository.save_config(current_config)
            
            return jsonify({
                "success": True,
                "message": "Configurações salvas com sucesso",
                "config": current_config.to_dict()
            })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/google-drive/setup", methods=["POST"])
@login_required
def setup_google_drive():
    """Setup Google Drive integration"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        data = request.get_json() or {}
        validated_data = BackupValidator.validate_google_drive_setup(data)
        
        success = backup_service.setup_google_drive(validated_data["credentials_file"])
        
        if success:
            return jsonify({
                "success": True,
                "message": "Google Drive configurado com sucesso"
            })
        else:
            return jsonify({
                "error": "Falha ao configurar Google Drive"
            }), 500
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@backup_bp.route("/api/backup/cleanup", methods=["POST"])
@login_required
def cleanup_old_backups():
    """Clean up old backups"""
    if current_user.role != "admin":
        return jsonify({"error": "Acesso negado"}), 403
    
    try:
        config = backup_repository.get_config()
        removed_count = backup_service.cleanup_old_backups(config.max_backups)
        
        return jsonify({
            "success": True,
            "message": f"{removed_count} backups antigos removidos",
            "removed_count": removed_count
        })
        
    except BackupError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500
