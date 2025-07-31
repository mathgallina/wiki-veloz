import json
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app.shared.decorators import admin_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/")
@login_required
@admin_required
def index():
    """Analytics dashboard page"""
    return render_template("admin_analytics.html")


@analytics_bp.route("/api/overview")
@login_required
@admin_required
def get_analytics_overview():
    """Retorna dados gerais de analytics"""
    try:
        # Carregar dados
        pages = load_pages()
        users = load_users()

        # Tentar carregar logs de atividade
        try:
            with open("app/data/activity_log.json", encoding="utf-8") as f:
                activities = json.load(f)
        except FileNotFoundError:
            activities = []

        # Estatísticas gerais
        total_pages = len(pages)
        total_users = len(users)
        active_users = sum(1 for user in users if user.get("is_active", True))
        admin_users = sum(1 for user in users if user["role"] == "admin")

        # Atividades dos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activities = [
            activity
            for activity in activities
            if datetime.fromisoformat(activity["timestamp"]) > thirty_days_ago
        ]

        # Páginas mais acessadas (simulado baseado em visualizações)
        page_views = {}
        for activity in activities:
            if activity["action"] == "page_view":
                details = activity["details"]
                page_title = (
                    details.split(": ")[-1]
                    if ": " in details
                    else "Página"
                )
                page_views[page_title] = page_views.get(page_title, 0) + 1

        top_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)[:5]

        # Atividades por tipo
        activity_types = {}
        for activity in recent_activities:
            action = activity["action"]
            activity_types[action] = activity_types.get(action, 0) + 1

        # Usuários mais ativos
        user_activity = {}
        for activity in recent_activities:
            user_id = activity["user_id"]
            user_activity[user_id] = user_activity.get(user_id, 0) + 1

        # Encontrar nomes dos usuários mais ativos
        top_users = []
        sorted_users = sorted(
            user_activity.items(), key=lambda x: x[1], reverse=True
        )[:5]
        for user_id, count in sorted_users:
            user = next((u for u in users if u["id"] == user_id), None)
            if user:
                top_users.append(
                    {
                        "name": user["name"],
                        "username": user["username"],
                        "activity_count": count,
                    }
                )

        # Crescimento de páginas por mês
        pages_by_month = {}
        for page in pages:
            created_date = datetime.fromisoformat(page["created_at"])
            month_key = created_date.strftime("%Y-%m")
            pages_by_month[month_key] = pages_by_month.get(month_key, 0) + 1

        # Últimas atividades
        latest_activities = sorted(
            activities, key=lambda x: x["timestamp"], reverse=True
        )[:10]

        return jsonify(
            {
                "overview": {
                    "total_pages": total_pages,
                    "total_users": total_users,
                    "active_users": active_users,
                    "admin_users": admin_users,
                    "recent_activities": len(recent_activities),
                },
                "top_pages": [
                    {"title": title, "views": views} for title, views in top_pages
                ],
                "activity_types": activity_types,
                "top_users": top_users,
                "pages_by_month": pages_by_month,
                "latest_activities": latest_activities,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/api/page-details")
@login_required
@admin_required
def get_page_analytics():
    """Retorna analytics detalhados das páginas"""
    try:
        pages = load_pages()

        # Estatísticas por categoria
        categories = {}
        for page in pages:
            category = page["category"]
            if category not in categories:
                categories[category] = {"count": 0, "pages": []}
            categories[category]["count"] += 1
            categories[category]["pages"].append(
                {
                    "id": page["id"],
                    "title": page["title"],
                    "created_at": page["created_at"],
                    "updated_at": page["updated_at"],
                }
            )

        # Páginas mais recentes
        recent_pages = sorted(pages, key=lambda x: x["updated_at"], reverse=True)[:10]

        # Páginas por tamanho (aproximado)
        pages_by_size = []
        for page in pages:
            content_length = len(page["content"])
            size_category = (
                "Pequena"
                if content_length < 1000
                else "Média"
                if content_length < 5000
                else "Grande"
            )
            pages_by_size.append(
                {
                    "title": page["title"],
                    "size": size_category,
                    "length": content_length,
                }
            )

        return jsonify(
            {
                "categories": categories,
                "recent_pages": recent_pages,
                "pages_by_size": pages_by_size,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/api/user-details")
@login_required
@admin_required
def get_user_analytics():
    """Retorna analytics detalhados dos usuários"""
    try:
        users = load_users()

        try:
            with open("app/data/activity_log.json", encoding="utf-8") as f:
                activities = json.load(f)
        except FileNotFoundError:
            activities = []

        # Atividade por usuário
        user_activity = {}
        for activity in activities:
            user_id = activity["user_id"]
            if user_id not in user_activity:
                user_activity[user_id] = {
                    "total_actions": 0,
                    "actions": {},
                    "last_activity": None,
                }

            user_activity[user_id]["total_actions"] += 1
            action = activity["action"]
            user_activity[user_id]["actions"][action] = user_activity[user_id]["actions"].get(action, 0) + 1

            # Atualizar última atividade
            activity_time = datetime.fromisoformat(activity["timestamp"])
            if (user_activity[user_id]["last_activity"] is None or 
                activity_time > datetime.fromisoformat(user_activity[user_id]["last_activity"])):
                user_activity[user_id]["last_activity"] = activity["timestamp"]

        # Combinar dados de usuário com atividade
        user_details = []
        for user in users:
            activity_data = user_activity.get(user["id"], {
                "total_actions": 0,
                "actions": {},
                "last_activity": None,
            })
            
            user_details.append({
                "id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "role": user["role"],
                "is_active": user.get("is_active", True),
                "created_at": user["created_at"],
                "total_actions": activity_data["total_actions"],
                "actions": activity_data["actions"],
                "last_activity": activity_data["last_activity"],
            })

        return jsonify({"users": user_details})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route("/api/export")
@login_required
@admin_required
def export_analytics():
    """Exporta todos os dados de analytics"""
    try:
        pages = load_pages()
        users = load_users()
        
        try:
            with open("app/data/activity_log.json", encoding="utf-8") as f:
                activities = json.load(f)
        except FileNotFoundError:
            activities = []

        export_data = {
            "export_date": datetime.now().isoformat(),
            "pages": pages,
            "users": users,
            "activities": activities,
            "summary": {
                "total_pages": len(pages),
                "total_users": len(users),
                "total_activities": len(activities),
                "active_users": sum(1 for user in users if user.get("is_active", True)),
                "admin_users": sum(1 for user in users if user["role"] == "admin"),
            }
        }

        return jsonify(export_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def load_pages():
    """Carrega dados das páginas"""
    try:
        with open("app/data/pages.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def load_users():
    """Carrega dados dos usuários"""
    try:
        with open("app/data/users.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
