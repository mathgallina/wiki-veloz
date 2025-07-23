"""
Rotas para documentos corporations
"""
import logging

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user

from app.modules.documents.services import DocumentService
from app.modules.documents.validators import DocumentValidator
from app.shared.decorators import login_required

logger = logging.getLogger(__name__)

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")
documents_service = DocumentService()
validator = DocumentValidator()


@documents_bp.route("/", methods=["GET"])
@login_required
def index():
    """Página principal de documentos"""
    return render_template("documents/index.html")


@documents_bp.route("/api/documents", methods=["GET"])
@login_required
def get_documents():
    """API para listar documentos"""
    try:
        documents = documents_service.get_all_documents()
        return (
            jsonify({"success": True, "data": [doc.to_dict() for doc in documents]}),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao buscar documentos: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents", methods=["POST"])
@login_required
def create_document():
    """API para criar documento"""
    try:
        data = request.get_json()

        # Validar dados
        validation_result = validator.validate_document_data(data)
        if not validation_result.is_valid:
            return (
                jsonify({"success": False, "message": validation_result.errors}),
                400,
            )

        # Adicionar author
        data["author"] = (
            current_user.name if current_user.is_authenticated else "Sistema"
        )

        document = documents_service.create_document(data)

        return (
            jsonify(
                {
                    "success": True,
                    "data": document.to_dict(),
                    "message": "Documento criado com sucesso",
                }
            ),
            201,
        )
    except Exception as e:
        logger.error(f"Error ao criar documento: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>", methods=["GET"])
@login_required
def get_document(document_id):
    """API para buscar documento específico"""
    try:
        document = documents_service.get_document(document_id)
        if not document:
            return (
                jsonify({"success": False, "message": "Documento não encontrado"}),
                404,
            )

        # Registrar visualização
        user_id = current_user.id if current_user.is_authenticated else None
        documents_service.record_view(document_id, user_id)

        return jsonify({"success": True, "data": document.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error ao buscar documento: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>", methods=["PUT"])
@login_required
def update_document(document_id):
    """API para atualizar documento"""
    try:
        data = request.get_json()

        # Validar dados
        validation_result = validator.validate_document_update(data)
        if not validation_result.is_valid:
            return (
                jsonify({"success": False, "message": validation_result.errors}),
                400,
            )

        # Adicionar author
        data["author"] = (
            current_user.name if current_user.is_authenticated else "Sistema"
        )

        document = documents_service.update_document(document_id, data)
        if not document:
            return (
                jsonify({"success": False, "message": "Documento não encontrado"}),
                404,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "data": document.to_dict(),
                    "message": "Documento atualizado com sucesso",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao atualizar documento: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>", methods=["DELETE"])
@login_required
def delete_document(document_id):
    """API para excluir documento"""
    try:
        success = documents_service.delete_document(document_id)
        if not success:
            return (
                jsonify({"success": False, "message": "Documento não encontrado"}),
                404,
            )

        return (
            jsonify({"success": True, "message": "Documento excluído com sucesso"}),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao excluir documento: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>/versions", methods=["GET"])
@login_required
def get_document_versions(document_id):
    """API para buscar versões de um documento"""
    try:
        versions = documents_service.get_document_versions(document_id)
        return (
            jsonify(
                {"success": True, "data": [version.to_dict() for version in versions]}
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao buscar versões: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/categories", methods=["GET"])
@login_required
def get_categories():
    """API para listar categorias"""
    try:
        categories = documents_service.get_all_categories()
        return (
            jsonify(
                {
                    "success": True,
                    "data": [category.to_dict() for category in categories],
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao buscar categorias: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/categories", methods=["POST"])
@login_required
def create_category():
    """API para criar categoria"""
    try:
        data = request.get_json()

        # Validar dados
        validation_result = validator.validate_category_data(data)
        if not validation_result.is_valid:
            return (
                jsonify({"success": False, "message": validation_result.errors}),
                400,
            )

        category = documents_service.create_category(data)

        return (
            jsonify(
                {
                    "success": True,
                    "data": category.to_dict(),
                    "message": "Categoria criada com sucesso",
                }
            ),
            201,
        )
    except Exception as e:
        logger.error(f"Error ao criar categoria: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


# Rotas para Analytics e Métricas
@documents_bp.route("/api/documents/<document_id>/view", methods=["POST"])
@login_required
def record_view(document_id):
    """API para registrar visualização de documento"""
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        documents_service.record_view(document_id, user_id)

        return jsonify({"success": True, "message": "Visualização registrada"}), 200
    except Exception as e:
        logger.error(f"Error ao registrar visualização: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>/download", methods=["POST"])
@login_required
def record_download(document_id):
    """API para registrar download de documento"""
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        documents_service.record_download(document_id, user_id)

        return jsonify({"success": True, "message": "Download registrado"}), 200
    except Exception as e:
        logger.error(f"Error ao registrar download: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>/analytics", methods=["GET"])
@login_required
def get_document_analytics(document_id):
    """API para buscar analytics de um documento"""
    try:
        analytics = documents_service.get_document_analytics(document_id)
        return jsonify({"success": True, "data": analytics}), 200
    except Exception as e:
        logger.error(f"Error ao buscar analytics: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/dashboard", methods=["GET"])
@login_required
def get_dashboard_stats():
    """API para buscar estatísticas do dashboard"""
    try:
        stats = documents_service.get_dashboard_stats()
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        logger.error(f"Error ao buscar estatísticas: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/analytics/user/<user_id>", methods=["GET"])
@login_required
def get_user_analytics(user_id):
    """API para buscar analytics de um usuário"""
    try:
        analytics = documents_service.get_user_analytics(user_id)
        return jsonify({"success": True, "data": analytics}), 200
    except Exception as e:
        logger.error(f"Error ao buscar analytics do usuário: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/reports/<report_type>", methods=["GET"])
@login_required
def generate_report(report_type):
    """API para gerar relatórios"""
    try:
        filters = request.args.to_dict()

        # Converter tipos de dados
        if "days" in filters:
            filters["days"] = int(filters["days"])

        report = documents_service.generate_report(report_type, filters)

        if "error" in report:
            return jsonify({"success": False, "message": report["error"]}), 400

        return jsonify({"success": True, "data": report}), 200
    except Exception as e:
        logger.error(f"Error ao gerar relatório: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Página do dashboard de analytics"""
    return render_template("documents/dashboard.html")


@documents_bp.route("/reports", methods=["GET"])
@login_required
def reports():
    """Página de relatórios"""
    return render_template("documents/reports.html")


# Rotas para Anexos
@documents_bp.route("/api/documents/<document_id>/attachments", methods=["GET"])
@login_required
def get_document_attachments(document_id):
    """API para buscar anexos de um documento"""
    try:
        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()
        attachments = attachment_service.get_document_attachments(document_id)
        return jsonify({"success": True, "data": attachments}), 200
    except Exception as e:
        logger.error(f"Error ao buscar anexos: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>/attachments", methods=["POST"])
@login_required
def upload_attachment(document_id):
    """API para fazer upload de anexo"""
    try:
        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()

        if "file" not in request.files:
            return jsonify({"success": False, "message": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        description = request.form.get("description", "")
        uploaded_by = current_user.name if current_user.is_authenticated else "Sistema"

        attachment = attachment_service.upload_attachment(
            file, document_id, description, uploaded_by
        )

        if not attachment:
            return (
                jsonify(
                    {"success": False, "message": "Error ao fazer upload do arquivo"}
                ),
                400,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "data": attachment,
                    "message": "Anexo enviado com sucesso",
                }
            ),
            201,
        )
    except Exception as e:
        logger.error(f"Error ao fazer upload de anexo: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/attachments/<attachment_id>", methods=["DELETE"])
@login_required
def delete_attachment(attachment_id):
    """API para deletar anexo"""
    try:
        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()

        success = attachment_service.delete_attachment(attachment_id)

        if not success:
            return jsonify({"success": False, "message": "Anexo não encontrado"}), 404

        return jsonify({"success": True, "message": "Anexo deletado com sucesso"}), 200
    except Exception as e:
        logger.error(f"Error ao deletar anexo: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/attachments/<attachment_id>", methods=["PUT"])
@login_required
def update_attachment_description(attachment_id):
    """API para atualizar descrição do anexo"""
    try:
        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()

        data = request.get_json()
        description = data.get("description", "")

        attachment = attachment_service.update_attachment_description(
            attachment_id, description
        )

        if not attachment:
            return jsonify({"success": False, "message": "Anexo não encontrado"}), 404

        return (
            jsonify(
                {
                    "success": True,
                    "data": attachment,
                    "message": "Descrição atualizada com sucesso",
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error ao atualizar descrição do anexo: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/<document_id>/attachments/stats", methods=["GET"])
@login_required
def get_attachment_stats(document_id):
    """API para buscar estatísticas dos anexos"""
    try:
        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()

        stats = attachment_service.get_attachment_stats(document_id)
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        logger.error(f"Error ao buscar estatísticas dos anexos: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route(
    "/api/documents/attachments/<attachment_id>/download", methods=["GET"]
)
@login_required
def download_attachment(attachment_id):
    """API para download de anexo"""
    try:
        import os

        from flask import send_file

        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()
        attachment = attachment_service.get_attachment(attachment_id)

        if not attachment:
            return jsonify({"success": False, "message": "Anexo não encontrado"}), 404

        if not os.path.exists(attachment["file_path"]):
            return jsonify({"success": False, "message": "Arquivo não encontrado"}), 404

        return send_file(
            attachment["file_path"],
            as_attachment=True,
            download_name=attachment["original_filename"],
            mimetype=attachment["mime_type"],
        )
    except Exception as e:
        logger.error(f"Error ao fazer download do anexo: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500


@documents_bp.route("/api/documents/attachments/<attachment_id>/view", methods=["GET"])
@login_required
def view_attachment(attachment_id):
    """API para visualizar anexo (sem download)"""
    try:
        import os

        from flask import send_file

        from app.modules.documents.attachment_service import AttachmentService

        attachment_service = AttachmentService()
        attachment = attachment_service.get_attachment(attachment_id)

        if not attachment:
            return jsonify({"success": False, "message": "Anexo não encontrado"}), 404

        if not os.path.exists(attachment["file_path"]):
            return jsonify({"success": False, "message": "Arquivo não encontrado"}), 404

        # Para PDFs, mostrar no navegador
        if attachment["mime_type"] == "application/pdf":
            return send_file(attachment["file_path"], mimetype="application/pdf")

        # Para imagens, mostrar no navegador
        elif attachment["mime_type"].startswith("image/"):
            return send_file(attachment["file_path"], mimetype=attachment["mime_type"])

        # Para outros tipos, forçar download
        else:
            return send_file(
                attachment["file_path"],
                as_attachment=True,
                download_name=attachment["original_filename"],
                mimetype=attachment["mime_type"],
            )
    except Exception as e:
        logger.error(f"Error ao visualizar anexo: {e}")
        return jsonify({"success": False, "message": "Error interno do servidor"}), 500
