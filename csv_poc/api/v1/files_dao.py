"""Data access library for Files API Namespace"""
from typing import List
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import csv
import os
from pathlib import Path

from csv_poc.extensions import db
from csv_poc.database.models import File, Column
from csv_poc.utils.exc import (
    InvalidMetadataException,
    InvalidFileTypeException,
    UnreadableFileException,
    DatabaseOpsException,
    FileNotFoundException,
    FilesystemException,
)
from csv_poc.utils.file import parse_columns

from sqlalchemy.exc import OperationalError, IntegrityError


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


class FileDAO(object):
    """DAO for handling CSV file data"""

    @staticmethod
    def list_files(**kwargs) -> List[File]:
        """Retrieves a list of all files in the database.

        This method returns basic data (everything except the columns) on all
        files stored in the database

        Args:
            **kwargs: TODO potential to be used for query parameters (filtering)

        Returns:
            A list of File objects, without their `columns` property.

        Raises:
            DatabaseOpsException: Error occurred while accessing the database
        """
        try:
            files = [file.to_dict() for file in File.query.all()]
            return files
        except OperationalError as oe:
            raise DatabaseOpsException(
                message="Error occurred while retrieving file list!",
                data=str(oe),
            )

    @staticmethod
    def add_file(file_storage: FileStorage):
        """Logic for uploading a CSV file

        This method performs a small number of functions:
        - validate file extension
        - write file to upload folder
        - make sure the file can be read by the csv library
        - analyze the column types in the CSV file

        Args:
            file_storage: Instance of `FileStorage` passed in from flask-restx's
              argument parser

        Raises:
            InvalidFileTypeException: Splits the file name and attempts to parse
              the file extension. Plain text string comparison.

            FilesystemException: If the file can not be written to the local
              filesystem

            UnreadableFileException: If the saved file can not be read by
              Python's native CSV library, this will be raised
        """
        if not allowed_file(file_storage.filename):
            raise InvalidFileTypeException(
                message=f"Invalid file type for file {file_storage.filename}",
                data=None,
            )
        safe_filename = secure_filename(file_storage.filename)
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], safe_filename
        )
        current_app.logger.debug(
            f"Created safe filename {safe_filename} for uploaded document"
        )

        # attempt to save the file to the server
        try:
            # make sure the folder exists first
            Path(current_app.config["UPLOAD_FOLDER"]).mkdir(
                parents=True, exist_ok=True
            )

            current_app.logger.debug(
                f"Saving file to folder {current_app.config['UPLOAD_FOLDER']}"
            )
            file_storage.save(file_path)
            file = File.create(name=safe_filename, path=file_path)

            # this method creates Column instances and adds them to the database
            # session, but does not commit them so we need to commit all columns
            # once complete
            parse_columns(file_path=file_path, file_id=file.id)
            db.session.commit()

            return file.to_dict(show=["columns", "path"])

        except IntegrityError as ie:
            raise DatabaseOpsException(
                message=f"File already exists", data=str(ie)
            )

        except Exception as e:
            raise FilesystemException(
                message="Unknown error occurred while saving file to server",
                data=str(e),
            )

    @staticmethod
    def get_file(file_id: int, **kwargs):
        current_app.logger.debug(f"Looking up file with ID {file_id}")
        try:
            file = File.get_by_id(file_id)

            if file is None:
                raise FileNotFoundException(
                    message=f"File with ID {file_id} could not be found!",
                    data=None,
                )
            return file.to_dict(show=["columns", "path"])

        except OperationalError as oe:
            raise DatabaseOpsException(
                message=f"Error occurred while retrieving file with ID {file_id}!",
                data=str(oe),
            )
