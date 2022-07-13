"""Contains Blueprint and API (flask-restx) initialization

By defining an `Api` (from flask-restx) this application can render an
interactive Swagger page for testing the API.
"""
from flask import Blueprint

from flask_restx import Api

from .files_ns import ns as files_ns

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1, version="1.0", title="CSV PoC API")

api.add_namespace(files_ns, path="/files")
