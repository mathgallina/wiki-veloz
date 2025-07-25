"""
Activity routes for Wiki Veloz
CDD v2.0 - Activity logging routes
"""

import json
from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.shared.decorators import admin_required

activity_bp = Blueprint("activity", __name__)


@activity_bp.route("/admin/activity")
@login_required
@admin_required
def admin_activity():
    """Admin activity page"""
    try:
        with open("app/data/activity_log.json", encoding="utf-8") as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Ordenar por timestamp (mais recente primeiro)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)

    return render_template("admin_activity.html", activities=activities)


@activity_bp.route("/api/activity/log", methods=["POST"])
@login_required
def log_activity():
    """Log activity endpoint"""
    from app.modules.activity.services.activity_service import ActivityService
    
    try:
        data = request.get_json()
        user_id = data.get("user_id", current_user.id)
        action = data.get("action")
        details = data.get("details")
        
        if not action:
            return {"error": "Action is required"}, 400
            
        activity_service = ActivityService()
        activity_service.log_activity(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        
        return {"success": True, "message": "Activity logged successfully"}
    except Exception as e:
        return {"error": str(e)}, 500


@activity_bp.route("/api/activity/list")
@login_required
@admin_required
def get_activities():
    """Get activities list"""
    try:
        with open("app/data/activity_log.json", encoding="utf-8") as f:
            activities = json.load(f)
    except FileNotFoundError:
        activities = []

    # Ordenar por timestamp (mais recente primeiro)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Limitar a 100 atividades mais recentes
    activities = activities[:100]
    
    return {"activities": activities} 