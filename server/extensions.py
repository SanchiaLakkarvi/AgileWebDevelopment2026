"""Shared Flask extensions.

Keep extension instances in one place to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# SQLAlchemy instance is initialized in create_app().
db = SQLAlchemy()
mail = Mail()
