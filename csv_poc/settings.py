"""File used for configuring all aspects of this Flask application

All "default" values in this file are settings for a production environment.
"""
import os
from environs import Env

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")

env = Env()
env.read_env()

# Flask Settings
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
UPLOAD_FOLDER = env.str(
    "UPLOAD_FOLDER", default=os.path.join(PROJECT_ROOT, "uploads")
)
ALLOWED_EXTENSIONS = {"csv"}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
SERVER_NAME = env.str("SERVER_NAME", default="server")

# Database Settings
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URI", default="sqlite://")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool(
    "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
)

# Logging
LOG_TO_STDOUT = env.bool("LOG_TO_STDOUT", default=False)

# Swagger / RestX Settings
SWAGGER_UI_DOC_EXPANSION = "list"
RESTX_MASK_SWAGGER = False
