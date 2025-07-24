"""
Authentication module for Wiki Veloz
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes
