from .routes import analytics_bp


def create_module(app):
    app.register_blueprint(analytics_bp)
