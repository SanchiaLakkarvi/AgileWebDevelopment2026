"""Application factory for the backend server."""

import os
from pathlib import Path

from flask import Flask

from server.extensions import db, mail
from server.routes.forum import forum_bp
from server.routes.marketplace import marketplace_bp


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def ensure_forum_schema() -> None:
    """Apply minimal schema patch for local SQLite without migrations."""

    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(posts)")
        columns = {row[1] for row in cursor.fetchall()}
        if "author_email" not in columns:
            cursor.execute("ALTER TABLE posts ADD COLUMN author_email VARCHAR(120)")
            conn.commit()
    finally:
        conn.close()


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
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", os.getenv("SMTP_HOST", ""))
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", os.getenv("SMTP_PORT", "587")))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "1") == "1"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "0") == "1"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", os.getenv("SMTP_USER", ""))
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", os.getenv("SMTP_PASS", ""))
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
        "MAIL_DEFAULT_SENDER",
        os.getenv("SMTP_FROM", os.getenv("MAIL_USERNAME", os.getenv("SMTP_USER", ""))),
    )
    # For this demo project, allow checked-in file config (mail_config.py) to override env vars.
    app.config.from_pyfile(str(BASE_DIR / "mail_config.py"), silent=True)

    # Bind extension and register feature blueprints.
    db.init_app(app)
    mail.init_app(app)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(forum_bp)

    with app.app_context():
        # Create schema on startup.
        db.create_all()
        ensure_forum_schema()

    return app
