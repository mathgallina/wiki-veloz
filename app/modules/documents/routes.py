"""
Document routes for Wiki Veloz
CDD v2.0 - Document endpoints
"""

import mimetypes
import os
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, send_file
from flask_login import current_user, login_required

from app.core.config import config
from app.core.database import DatabaseManager
from app.modules.documents.services.document_service import DocumentService

# Initialize services
db_manager = DatabaseManager(config['default']())
document_service = DocumentService(db_manager)

documents_bp = Blueprint("documents", __name__)


@documents_bp.route("/", methods=["GET"])
@login_required
def get_documents():
    """Get documents web interface"""
    return render_template("documents/index.html")

@documents_bp.route("/api/", methods=["GET"])
@login_required
def get_documents_api():
    """Get all documents API"""
    try:
        documents = document_service.get_all_documents()
        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>", methods=["GET"])
@login_required
def get_document(document_id):
    """Get document by ID"""
    try:
        document = document_service.get_document_by_id(document_id)

        if document:
            return jsonify({
                "success": True,
                "data": document
            })
        else:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/create", methods=["POST"])
@login_required
def create_document_json():
    """Create new document with optional file upload"""
    try:
        # Check if this is a multipart form (file upload) or JSON
        if (request.content_type and 
            'multipart/form-data' in request.content_type):
            # Handle file upload
            document_data = {
                'title': request.form.get('title', ''),
                'description': request.form.get('description', ''),
                'category': request.form.get('category', ''),
                'content': request.form.get('content', ''),
                'type': request.form.get('type', 'documento'),
                'priority': request.form.get('priority', 'media'),
                'author': request.form.get('author', current_user.id),
                'tags': request.form.get('tags', '').split(',') if request.form.get('tags') else [],
                'page_id': request.form.get('page_id', '')
            }
            
            # Check if file was uploaded
            file = None
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    file = None  # No file selected
            
            success, message = document_service.create_document(
                document_data,
                file,
                current_user.id
            )
        else:
            # Handle JSON request (without file)
            document_data = request.get_json()
            
            if not document_data:
                return jsonify({
                    "success": False,
                    "message": "Dados do documento são obrigatórios"
                }), 400

            # Add required fields
            document_data['author'] = current_user.id
            document_data['created_at'] = datetime.now().isoformat()
            document_data['updated_at'] = datetime.now().isoformat()
            document_data['version'] = 1
            document_data['status'] = 'ativo'

            success, message = document_service.create_document_json(
                document_data
            )

        if success:
            return jsonify({
                "success": True,
                "message": message
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/", methods=["POST"])
@login_required
def create_document():
    """Create new document with file upload"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "Arquivo é obrigatório"
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "message": "Nenhum arquivo selecionado"
            }), 400

        # Get form data
        document_data = {
            'title': request.form.get('title', ''),
            'description': request.form.get('description', ''),
            'category': request.form.get('category', ''),
            'tags': request.form.get('tags', '').split(',') if request.form.get('tags') else [],
            'page_id': request.form.get('page_id', '')
        }

        success, message = document_service.create_document(
            document_data,
            file,
            current_user.id
        )

        if success:
            return jsonify({
                "success": True,
                "message": message
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>", methods=["PUT"])
@login_required
def update_document(document_id):
    """Update document"""
    try:
        updates = request.get_json()

        if not updates:
            return jsonify({
                "success": False,
                "message": "Dados de atualização são obrigatórios"
            }), 400

        success, message = document_service.update_document(
            document_id,
            updates,
            current_user.id
        )

        if success:
            return jsonify({
                "success": True,
                "message": message
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400 if "não encontrado" in message else 403

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>", methods=["DELETE"])
@login_required
def delete_document(document_id):
    """Delete document"""
    try:
        success, message = document_service.delete_document(
            document_id,
            current_user.id
        )

        if success:
            return jsonify({
                "success": True,
                "message": message
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400 if "não encontrado" in message else 403

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/search", methods=["GET"])
@login_required
def search_documents():
    """Search documents"""
    try:
        query = request.args.get("q", "")

        if not query:
            return jsonify({
                "success": False,
                "message": "Query obrigatória"
            }), 400

        results = document_service.search_documents(query)

        return jsonify({
            "success": True,
            "data": results,
            "count": len(results),
            "query": query
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/category/<category>", methods=["GET"])
@login_required
def get_documents_by_category(category):
    """Get documents by category"""
    try:
        documents = document_service.get_documents_by_category(category)

        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents),
            "category": category
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/author/<author_id>", methods=["GET"])
@login_required
def get_documents_by_author(author_id):
    """Get documents by author"""
    try:
        documents = document_service.get_documents_by_author(author_id)

        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents),
            "author_id": author_id
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/page/<page_id>", methods=["GET"])
@login_required
def get_documents_by_page(page_id):
    """Get documents by associated page"""
    try:
        documents = document_service.get_documents_by_page(page_id)

        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents),
            "page_id": page_id
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/recent", methods=["GET"])
@login_required
def get_recent_documents():
    """Get recent documents"""
    try:
        limit = int(request.args.get("limit", 10))
        documents = document_service.get_recent_documents(limit)

        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/popular", methods=["GET"])
@login_required
def get_popular_documents():
    """Get popular documents"""
    try:
        limit = int(request.args.get("limit", 10))
        documents = document_service.get_popular_documents(limit)

        return jsonify({
            "success": True,
            "data": documents,
            "count": len(documents)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/download", methods=["GET"])
@login_required
def download_document(document_id):
    """Download document file"""
    try:
        success, message, file_path = document_service.download_document(
            document_id,
            current_user.id
        )

        if success and file_path:
            return send_file(
                file_path,
                as_attachment=True,
                download_name=message
            )
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/view", methods=["GET"])
@login_required
def view_document_file(document_id):
    """View document file inline"""
    try:
        document = document_service.get_document_by_id(document_id)
        
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        # Check if document has a file
        if not document.get('filename'):
            return jsonify({
                "success": False,
                "message": "Documento não possui arquivo anexado"
            }), 404

        file_path = document_service.get_document_file_path(document_id)
        
        if not file_path:
            return jsonify({
                "success": False,
                "message": "Arquivo não encontrado. Verifique se o upload foi concluído corretamente."
            }), 404

        # Detect MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        # Return file for inline viewing
        return send_file(
            file_path,
            as_attachment=False,
            mimetype=mime_type
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/preview", methods=["GET"])
@login_required
def preview_document(document_id):
    """Get document preview information"""
    try:
        document = document_service.get_document_by_id(document_id)
        
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        # Add file information
        has_file = bool(document.get('filename'))
        file_path = None
        
        if has_file:
            file_path = document_service.get_document_file_path(document_id)
            has_file = file_path and os.path.exists(file_path)

        preview_data = {
            **document,
            "has_file": has_file,
            "file_path": file_path,
            "can_preview": has_file and (
                document.get('filename', '').lower().endswith('.pdf') or
                any(ext in document.get('filename', '').lower() 
                    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
            )
        }

        return jsonify({
            "success": True,
            "data": preview_data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/analytics", methods=["GET"])
@login_required
def get_document_analytics(document_id):
    """Get document analytics"""
    try:
        analytics = document_service.get_document_analytics(document_id)

        if analytics:
            return jsonify({
                "success": True,
                "data": analytics
            })
        else:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/analytics/storage", methods=["GET"])
@login_required
def get_storage_analytics():
    """Get storage analytics"""
    try:
        analytics = document_service.get_storage_analytics()

        return jsonify({
            "success": True,
            "data": analytics
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/sample/create", methods=["POST"])
@login_required
def create_sample_documents():
    """Create sample documents for testing"""
    try:
        # Only admin can create sample documents
        if current_user.role != "admin":
            return jsonify({
                "success": False,
                "message": "Apenas administradores podem criar documentos de exemplo"
            }), 403

        success = document_service.create_sample_documents()

        if success:
            return jsonify({
                "success": True,
                "message": "Documentos de exemplo criados com sucesso"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Erro ao criar documentos de exemplo"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


# Web routes
@documents_bp.route("/dashboard", methods=["GET"])
@login_required
def documents_dashboard():
    """Documents dashboard page"""
    return render_template("documents/dashboard.html")


@documents_bp.route("/<document_id>/confirm", methods=["POST"])
@login_required
def confirm_document_read(document_id):
    """Confirm document read by user"""
    try:
        # Check if document exists
        document = document_service.get_document_by_id(document_id)
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        # Check if user already confirmed this document
        confirmation = document_service.get_document_confirmation(document_id, current_user.id)
        if confirmation:
            return jsonify({
                "success": False,
                "message": "Você já confirmou a leitura deste documento"
            }), 400

        # Create confirmation
        success, message = document_service.confirm_document_read(
            document_id,
            current_user.id,
            request.remote_addr
        )

        if success:
            return jsonify({
                "success": True,
                "message": "Leitura confirmada com sucesso",
                "data": {
                    "document_id": document_id,
                    "user_id": current_user.id,
                    "confirmed_at": message
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/confirmation", methods=["GET"])
@login_required
def get_document_confirmation(document_id):
    """Get document confirmation status for current user"""
    try:
        # Check if document exists
        document = document_service.get_document_by_id(document_id)
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        # Get confirmation status
        confirmation = document_service.get_document_confirmation(document_id, current_user.id)

        return jsonify({
            "success": True,
            "data": {
                "document_id": document_id,
                "user_id": current_user.id,
                "confirmed": bool(confirmation),
                "confirmation": confirmation
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/edit", methods=["GET"])
@login_required
def edit_document_page(document_id):
    """Edit document page - Admin only"""
    try:
        # Check if user is admin
        if current_user.role != "admin":
            return jsonify({
                "success": False,
                "message": "Apenas administradores podem editar documentos"
            }), 403

        # Get document data
        document = document_service.get_document_by_id(document_id)
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        return render_template("documents/edit.html", document=document)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@documents_bp.route("/<document_id>/edit", methods=["POST"])
@login_required
def update_document_with_file(document_id):
    """Update document with optional file upload - Admin only"""
    try:
        # Check if user is admin
        if current_user.role != "admin":
            return jsonify({
                "success": False,
                "message": "Apenas administradores podem editar documentos"
            }), 403

        # Check if document exists
        document = document_service.get_document_by_id(document_id)
        if not document:
            return jsonify({
                "success": False,
                "message": "Documento não encontrado"
            }), 404

        # Prepare update data
        updates = {
            'title': request.form.get('title', ''),
            'description': request.form.get('description', ''),
            'category': request.form.get('category', ''),
            'updated_at': datetime.now().isoformat(),
            'updated_by': current_user.id
        }

        # Handle file upload if provided
        file = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                file = None  # No file selected

        # Update document with file
        success, message = document_service.update_document_with_file(
            document_id,
            updates,
            file,
            current_user.id
        )

        if success:
            return jsonify({
                "success": True,
                "message": message
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500
