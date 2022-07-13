"""Central file for creating and configuring Flask instances.

This file is not intended to be used directly, rather another module should
import and call "create_app()" in order to start the Flask development server.

  Typical usage example:

  from csv_poc.app import create_app
  app = create_app()

"""
import logging
import os
import pprint
from logging.handlers import RotatingFileHandler

from flask import Flask

from csv_poc.extensions import db, migrate
from csv_poc.api.v1 import api_v1


def create_app(config_obj="csv_poc.settings") -> Flask:
    """
    Factory-style method for creating a Flask application. This method is
    responsible for not only initializing the app, but also calling/setting up
    all extensions and Blueprints used.

    Args:
        config_obj: String representation of the path to the Python file with
          settings for this application.

    Returns:
        A fully-configured Flask instance.

    """
    app = Flask(__name__.split(".", maxsplit=1)[0])
    app.config.from_object(config_obj)

    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    return app


def register_extensions(app: Flask) -> None:
    """Initializes all needed extensions

    Given the passed in Flask instance, this method calls an
    initialization method for all extensions that are needed. Generally,
    Flask's extensions follow a method name pattern of `init_app()`.

    Args:
        app: Flask instance
    """
    db.init_app(app)

    # conditionally set/use batch ops for migrations
    # https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite
    with app.app_context():
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    """Initializes all Blueprints

    Calls Flask's "register_blueprint()" method for each Blueprint used by
    this application.

    Args:
        app:
    """
    app.register_blueprint(api_v1)


def configure_logger(app: Flask) -> None:
    """Configures logging options for the application

    Args:
        app: Flask instance that needs logging configured.
    """
    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/csv-poc.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d] "
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG if app.config["DEBUG"] else logging.INFO)
    app.logger.info("CSV PoC API Initialized")
    app.logger.debug(f":: App Config ::\n{pprint.pformat(app.config)}")
