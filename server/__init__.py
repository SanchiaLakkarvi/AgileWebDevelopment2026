"""Application factory for the backend server."""

from pathlib import Path

from flask import Flask

from server.extensions import db
from server.forum.routes import forum_bp
from server.marketplace.routes import marketplace_bp


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def create_app() -> Flask:
    # Ensure local runtime directory exists before configuring SQLite path.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "src"),
        static_url_path="/static",
        template_folder=str(BASE_DIR / "templates"),
    )
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATA_DIR / 'forum.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Bind extension and register feature blueprints.
    db.init_app(app)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(forum_bp)

    with app.app_context():
        # Create schema on startup.
        db.create_all()

    return app
