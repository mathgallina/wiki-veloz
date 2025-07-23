from flask import Blueprint

backup_bp = Blueprint('backup', __name__, url_prefix='/backup')


@backup_bp.route('/')
def index():
    return {'message': 'Backup module funcionando!'}
