from flask import Blueprint, render_template
from flask_login import login_required

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/")
@login_required
def index():
    """Notifications management page"""
    return render_template("admin_notifications.html")
