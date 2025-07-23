from flask import Blueprint

pages_bp = Blueprint("pages", __name__, url_prefix="/pages")


@pages_bp.route("/")
def index():
    return {"message": "Pages module funcionando!"}
