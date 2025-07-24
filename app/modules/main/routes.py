"""
Main routes for Wiki Veloz
"""

from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
@login_required
def index():
    """Main dashboard page"""
    return render_template("index.html")


@main_bp.route("/admin/activity")
@login_required
def admin_activity():
    """Admin activity page"""
    return render_template("admin/activity.html")


@main_bp.route("/admin/analytics")
@login_required
def admin_analytics():
    """Admin analytics page"""
    return render_template("admin/analytics.html")


@main_bp.route("/admin/notifications")
@login_required
def admin_notifications():
    """Admin notifications page"""
    return render_template("admin/notifications.html")


@main_bp.route("/admin/pdfs")
@login_required
def admin_pdfs():
    """Admin PDFs page"""
    return render_template("admin/pdfs.html")


@main_bp.route("/admin/backup")
@login_required
def admin_backup():
    """Admin backup page"""
    return render_template("admin/backup.html")
