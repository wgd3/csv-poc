"""API Namespace for handling CSV files"""
from flask_restx import Resource, fields, Namespace
from http import HTTPStatus
from flask import current_app, request
from werkzeug.datastructures import FileStorage

from csv_poc.utils.exc import (
    InvalidMetadataException,
    InvalidFileTypeException,
    UnreadableFileException,
    DatabaseOpsException,
    FileNotFoundException,
    CsvPocException,
)

from .files_dao import FileDAO

ns = Namespace("files", description="CSV File Operations")

get_column_model = ns.model(
    "GetColumn",
    {
        "id": fields.Integer(
            description="Primary key for column object", readonly=True
        ),
        "col_index": fields.Integer(
            description="Index/position of column in " "CSV file"
        ),
        "col_name": fields.String(description="Column name"),
        "col_type": fields.String(
            enum=["text", "number", "datetime"], description="Column type"
        ),
    },
)

get_file_list_model = ns.model(
    "GetFileListModel",
    {
        "id": fields.Integer(
            description="Primary key for files object", readonly=True
        ),
        "name": fields.String(description="Name of the file"),
    },
)

get_file_model = ns.model(
    "GetFile",
    {
        "id": fields.Integer(
            description="Primary key for files object", readonly=True
        ),
        "name": fields.String(description="Name of the file"),
        "path": fields.String(description="Path to file on disk"),
        "columns": fields.List(fields.Nested(get_column_model)),
    },
)

error_model = ns.model(
    "HTTPError",
    {
        "message": fields.String(description="User-friendly error message"),
        "data": fields.Raw(description="Any data associated with an error"),
    },
)

upload_parser = ns.parser()
upload_parser.add_argument(
    "file", location="files", type=FileStorage, required=True
)


@ns.route("", endpoint="get_file_list")
class FileListResource(Resource):
    """Resource for handling file upload and retrieval

    This resource exposes 2 endpoints: the GET request for a list of files, and
    the POST request for uploading a new CSV file. In order to match REST API
    specifications, the POST endpoint uses "files" as the entity (in the plural)
    instead of POST-ing to a route such as `/upload`
    """

    # @ns.response(
    #     HTTPStatus.OK.value,
    #     HTTPStatus.OK.phrase,
    #     model=get_file_list_model,
    #     as_list=True,
    # )
    @ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR.value,
        HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        model=error_model,
    )
    @ns.marshal_with(get_file_list_model, as_list=True, code=HTTPStatus.OK)
    def get(self):
        """GET handler which returns a list of files in the database

        Returns:
            A list of files
        """
        current_app.logger.debug(f"Retrieving list of files...")
        try:
            files = FileDAO.list_files()
            return files, HTTPStatus.OK
        except DatabaseOpsException as dbe:
            current_app.logger.error(dbe.message)
            current_app.logger.error(dbe.data)
            return {
                "message": dbe.message,
                "data": dbe.data,
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    @ns.response(
        HTTPStatus.CREATED.value,
        HTTPStatus.CREATED.phrase,
        model=get_file_model,
    )
    @ns.response(
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase,
    )
    @ns.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @ns.expect(upload_parser)
    def post(self, **kwargs):
        """POST handler for file uploads

        Returns:
            Details for the file that was uploaded
        """
        try:
            args = upload_parser.parse_args()
            uploaded_file: FileStorage = args["file"]
            rv = FileDAO.add_file(uploaded_file)
            current_app.logger.debug(f"Returning data:\n{rv}")
            return rv, HTTPStatus.CREATED
        except DatabaseOpsException as dbe:
            return {
                "message": dbe.message,
                "data": dbe.data,
            }, HTTPStatus.BAD_REQUEST
        except CsvPocException as e:
            return {
                "message": e.message,
                "data": e.data,
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@ns.route("/<int:file_id>", endpoint="get_file")
class FileResource(Resource):
    """Resource for retrieving data on a single CSV file"""

    @ns.response(
        HTTPStatus.INTERNAL_SERVER_ERROR.value,
        HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        model=error_model,
    )
    @ns.response(
        HTTPStatus.NOT_FOUND.value,
        HTTPStatus.NOT_FOUND.phrase,
        model=error_model,
    )
    @ns.response(
        HTTPStatus.OK.value, HTTPStatus.OK.phrase, model=get_file_model
    )
    def get(self, file_id, **kwargs):
        """GET handler for returning the details on a single CSV file"""
        try:
            file = FileDAO.get_file(file_id, **kwargs)
            return file, HTTPStatus.OK
        except FileNotFoundException as fnf:
            current_app.logger.error(f"File with ID {file_id} not found!")
            return {
                "message": fnf.message,
                "data": fnf.data,
            }, HTTPStatus.NOT_FOUND
        except DatabaseOpsException as dbe:
            current_app.logger.error(
                f"Error retrieving file {file_id}: {dbe.message}"
            )
            return {
                "message": dbe.message,
                "data": dbe.data,
            }, HTTPStatus.INTERNAL_SERVER_ERROR
