from .routes import pdfs_bp


def create_module(app):
    app.register_blueprint(pdfs_bp)
