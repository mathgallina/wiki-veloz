from flask import Blueprint

pdfs_bp = Blueprint('pdfs', __name__, url_prefix='/pdfs')


@pdfs_bp.route('/')
def index():
    return {'message': 'PDFs module funcionando!'}
