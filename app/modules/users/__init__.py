from .routes import users_bp


def create_module(app):
    app.register_blueprint(users_bp)
