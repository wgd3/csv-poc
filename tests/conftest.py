"""Main test configuration file"""
import pytest
from pathlib import Path
from csv_poc.app import create_app
from flask import Flask

from csv_poc.extensions import db as _db

TEST_DIR = Path(__file__).parent


@pytest.fixture(autouse=True)
def app():
    """Creates an app instance to test with.

    Yields:
        A Flask app instance inside a test context.
    """
    _app = create_app(config_obj="tests.testing_settings")

    with _app.app_context():
        # _app.config.update(
        #     {
        #         "TESTING": True,
        #         "SQLALCHEMY_DATABASE"
        #     }
        # )
        yield _app


@pytest.fixture(autouse=True)
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(autouse=True)
def client(app: Flask):
    """Creates a Client which contains HTTP methods

    Args:
        app: Flask instance

    Returns:
        Flask client that can be used for HTTP requests
    """
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    """Creates an instance of FlaskCliRunner

    Used for testing CLI commands

    Args:
        app: Flask instance

    Returns:
        Runner for monitoring CLI command output
    """
    return app.test_cli_runner()
