"""
Main module for Wiki Veloz
"""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

from . import routes
