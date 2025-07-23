from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@analytics_bp.route('/')
def index():
    return {'message': 'Analytics module funcionando!'}
