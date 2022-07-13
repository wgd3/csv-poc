"""Data access library for Files API Namespace"""
from typing import List
from flask import current_app

from csv_poc.database.models import File, Column
from csv_poc.utils.exc import (
    InvalidMetadataException,
    InvalidFileTypeException,
    UnreadableFileException,
    DatabaseOpsException,
    FileNotFoundException,
)

from sqlalchemy.exc import OperationalError


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
            files = [file.to_json() for file in File.query.all()]
            return files
        except OperationalError as oe:
            raise DatabaseOpsException(
                message="Error occurred while retrieving file list!", data=str(oe)
            )

    @staticmethod
    def get_file(file_id: int, **kwargs):
        current_app.logger.debug(f"Looking up file with ID {file_id}")
        try:
            file = File.get_by_id(file_id)

            if file is None:
                raise FileNotFoundException(
                    message=f"File with ID {file_id} could not be found!", data=None
                )
            return file.to_json()

        except OperationalError as oe:
            raise DatabaseOpsException(
                message=f"Error occurred while retrieving file with ID {file_id}!",
                data=str(oe),
            )
