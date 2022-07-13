"""File declaring all extensions used by the application.

The pattern for Flask extensions is typically to create an instance of them at
some point before/after the Flask instance is created, and then run an
`init_app()` method for each extension at a later point.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
