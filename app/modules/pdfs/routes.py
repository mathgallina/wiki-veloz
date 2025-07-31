from flask import Blueprint, render_template
from flask_login import login_required

pdfs_bp = Blueprint("pdfs", __name__)


@pdfs_bp.route("/")
@login_required
def index():
    """PDFs management page"""
    return render_template("admin_pdfs.html")
