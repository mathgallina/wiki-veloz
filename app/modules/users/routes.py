from flask import Blueprint, render_template
from flask_login import login_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
@login_required
def index():
    """Users management page"""
    return render_template("admin_users.html")
