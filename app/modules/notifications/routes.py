from flask import Blueprint

notifications_bp = Blueprint(
    'notifications', __name__, url_prefix='/notifications'
)


@notifications_bp.route('/')
def index():
    return {'message': 'Notifications module funcionando!'}
