"""
Main routes for Wiki Veloz
CDD v2.0 - Main application routes
"""

import json

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    """Main dashboard page"""
    return render_template("index.html")


@main_bp.route("/pages")
@login_required
def pages():
    """Pages management page"""
    return render_template("pages/index.html")


@main_bp.route("/documents")
@login_required
def documents():
    """Documents dashboard page"""
    return render_template("documents/index.html")


@main_bp.route("/api/categories")
@login_required
def get_categories():
    """Get all categories from pages"""
    try:
        from app.core.config import config
        from app.core.database import DatabaseManager
        from app.modules.pages.services.page_service import PageService

        # Initialize services
        db_manager = DatabaseManager(config['default'])
        page_service = PageService(db_manager)
        
        # Get all pages
        pages = page_service.get_all_pages()
        
        # Extract unique categories
        categories = list({
            page.get("category", "geral") for page in pages
        })
        
        return jsonify(categories)
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@main_bp.route("/api/search")
@login_required
def global_search():
    """Global search endpoint - search pages and documents"""
    try:
        query = request.args.get("q", "").strip()
        
        if not query:
            return jsonify({
                "pages": [],
                "files": [],
                "total_results": 0
            })
        
        # Import services
        from app.core.config import config
        from app.core.database import DatabaseManager
        from app.modules.documents.services.document_service import DocumentService
        from app.modules.pages.services.page_service import PageService

        # Initialize services
        db_manager = DatabaseManager(config['default'])
        page_service = PageService(db_manager)
        document_service = DocumentService(db_manager)
        
        # Search pages
        page_results = page_service.search_pages(query)
        
        # Search documents
        document_results = document_service.search_documents(query)
        
        # Load PDFs for file search
        try:
            with open("app/data/pdfs.json", "r", encoding="utf-8") as f:
                pdfs = json.load(f)
        except FileNotFoundError:
            pdfs = []
        
        # Search in PDFs
        file_results = []
        query_lower = query.lower()
        for pdf in pdfs:
            if (query_lower in pdf.get("original_filename", "").lower() or
                query_lower in pdf.get("description", "").lower() or
                query_lower in pdf.get("sector_name", "").lower() or
                query_lower in pdf.get("trainer", "").lower()):
                file_results.append({**pdf, "type": "file"})
        
        total_results = len(page_results) + len(document_results) + len(
            file_results
        )
        
        # Log search activity
        try:
            from app.modules.activity.services.activity_service import ActivityService
            activity_service = ActivityService()
            activity_service.log_activity(
                current_user.id,
                "search",
                f"Pesquisou por: {query} ({total_results} resultados)"
            )
        except Exception as e:
            print(f"Error logging search activity: {e}")
        
        return jsonify({
            "pages": page_results,
            "documents": document_results,
            "files": file_results,
            "total_results": total_results,
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "pages": [],
            "files": [],
            "total_results": 0
        }), 500


@main_bp.route("/admin/analytics")
@login_required
def admin_analytics():
    """Admin analytics page"""
    return render_template("admin_analytics.html")


@main_bp.route("/admin/notifications")
@login_required
def admin_notifications():
    """Admin notifications page"""
    return render_template("admin_notifications.html")


@main_bp.route("/admin/pdfs")
@login_required
def admin_pdfs():
    """Admin PDFs page"""
    return render_template("admin_pdfs.html")


@main_bp.route("/admin/backup")
@login_required
def admin_backup():
    """Admin backup page"""
    return render_template("admin_backup.html")


@main_bp.route("/planos")
@login_required
def planos():
    """Planos Ultra Velocidade page"""
    return render_template("planos_veloz.html")
