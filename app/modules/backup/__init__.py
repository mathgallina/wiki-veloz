from .routes import backup_bp


def create_module(app):
    app.register_blueprint(backup_bp)
