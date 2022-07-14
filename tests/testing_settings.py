"""Configuration for testing"""
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")

TESTING = True
DEBUG = False
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "tmp/uploads")
ALLOWED_EXTENSIONS = {"csv"}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
SERVER_NAME = "server"

# Database Settings
SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Logging
LOG_TO_STDOUT = True

# Swagger / RestX Settings
SWAGGER_UI_DOC_EXPANSION = "list"
RESTX_MASK_SWAGGER = False
