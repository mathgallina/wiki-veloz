"""
Backup Module for Wiki Veloz
CDD v2.0 - Complete backup system
"""

from .routes import backup_bp

__all__ = ['backup_bp']


def create_module(app):
    app.register_blueprint(backup_bp)
