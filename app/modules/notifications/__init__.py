from .routes import notifications_bp


def create_module(app):
    app.register_blueprint(notifications_bp)
