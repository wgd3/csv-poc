"""Entrypoint for use in the Docker container version of the app

This is the same as `autoapp.py` in the project root, just located here so that
it's more easily moved into the Docker image at build time. It also adds
database commands to make sure tables are created and available as expected.
"""
from csv_poc.app import create_app
from csv_poc.extensions import db

app = create_app()
with app.app_context():
    app.logger.info("Making sure database is up to date...")
    db.create_all()
