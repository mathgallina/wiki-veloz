from .routes import pages_bp


def create_module(app):
    app.register_blueprint(pages_bp)
