"""
Page routes for Wiki Veloz
CDD v2.0 - Page endpoints
"""

from flask import Blueprint, jsonify, request, render_template
from flask_login import current_user, login_required

from app.core.database import DatabaseManager
from app.core.config import config
from app.modules.pages.services.page_service import PageService

# Initialize services
db_manager = DatabaseManager(config['default']())
page_service = PageService(db_manager)

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/", methods=["GET"])
@login_required
def get_pages():
    """Get all pages"""
    try:
        pages = page_service.get_all_pages()
        return jsonify({
            "success": True,
            "data": pages,
            "count": len(pages)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/<page_id>", methods=["GET"])
@login_required
def get_page(page_id):
    """Get page by ID"""
    try:
        page = page_service.get_page_by_id(page_id)
        
        if page:
            return jsonify({
                "success": True,
                "data": page
            })
        else:
            return jsonify({
                "success": False,
                "message": "Página não encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/slug/<slug>", methods=["GET"])
@login_required
def get_page_by_slug(slug):
    """Get page by slug"""
    try:
        page = page_service.get_page_by_slug(slug)
        
        if page:
            return jsonify({
                "success": True,
                "data": page
            })
        else:
            return jsonify({
                "success": False,
                "message": "Página não encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/", methods=["POST"])
@login_required
def create_page():
    """Create new page"""
    try:
        page_data = request.get_json()
        
        if not page_data:
            return jsonify({
                "success": False,
                "message": "Dados da página são obrigatórios"
            }), 400
        
        success, message = page_service.create_page(
            page_data, 
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


@pages_bp.route("/<page_id>", methods=["PUT"])
@login_required
def update_page(page_id):
    """Update page"""
    try:
        updates = request.get_json()
        
        if not updates:
            return jsonify({
                "success": False,
                "message": "Dados de atualização são obrigatórios"
            }), 400
        
        success, message = page_service.update_page(
            page_id, 
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
            }), 400 if "não encontrada" in message else 403
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/<page_id>", methods=["DELETE"])
@login_required
def delete_page(page_id):
    """Delete page"""
    try:
        success, message = page_service.delete_page(
            page_id, 
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
            }), 400 if "não encontrada" in message else 403
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/search", methods=["GET"])
@login_required
def search_pages():
    """Search pages"""
    try:
        query = request.args.get("q", "")
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query de busca é obrigatória"
            }), 400
        
        results = page_service.search_pages(query)
        
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


@pages_bp.route("/category/<category>", methods=["GET"])
@login_required
def get_pages_by_category(category):
    """Get pages by category"""
    try:
        pages = page_service.get_pages_by_category(category)
        
        return jsonify({
            "success": True,
            "data": pages,
            "count": len(pages),
            "category": category
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/author/<author_id>", methods=["GET"])
@login_required
def get_pages_by_author(author_id):
    """Get pages by author"""
    try:
        pages = page_service.get_pages_by_author(author_id)
        
        return jsonify({
            "success": True,
            "data": pages,
            "count": len(pages),
            "author_id": author_id
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/recent", methods=["GET"])
@login_required
def get_recent_pages():
    """Get recent pages"""
    try:
        limit = int(request.args.get("limit", 10))
        pages = page_service.get_recent_pages(limit)
        
        return jsonify({
            "success": True,
            "data": pages,
            "count": len(pages)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/popular", methods=["GET"])
@login_required
def get_popular_pages():
    """Get popular pages"""
    try:
        limit = int(request.args.get("limit", 10))
        pages = page_service.get_popular_pages(limit)
        
        return jsonify({
            "success": True,
            "data": pages,
            "count": len(pages)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/<page_id>/versions", methods=["GET"])
@login_required
def get_page_versions(page_id):
    """Get page versions"""
    try:
        versions = page_service.get_page_versions(page_id)
        
        return jsonify({
            "success": True,
            "data": versions,
            "count": len(versions),
            "page_id": page_id
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/<page_id>/versions/<int:version>/restore", methods=["POST"])
@login_required
def restore_page_version(page_id, version):
    """Restore page version"""
    try:
        success, message = page_service.restore_page_version(
            page_id, 
            version, 
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
            }), 400 if "não encontrada" in message else 403
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/<page_id>/analytics", methods=["GET"])
@login_required
def get_page_analytics(page_id):
    """Get page analytics"""
    try:
        analytics = page_service.get_page_analytics(page_id)
        
        if analytics:
            return jsonify({
                "success": True,
                "data": analytics
            })
        else:
            return jsonify({
                "success": False,
                "message": "Página não encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500


@pages_bp.route("/sample/create", methods=["POST"])
@login_required
def create_sample_pages():
    """Create sample pages for testing"""
    try:
        # Only admin can create sample pages
        if current_user.role != "admin":
            return jsonify({
                "success": False,
                "message": "Apenas administradores podem criar páginas de exemplo"
            }), 403
        
        success = page_service.create_sample_pages()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Páginas de exemplo criadas com sucesso"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Erro ao criar páginas de exemplo"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500
