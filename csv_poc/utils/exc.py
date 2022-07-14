"""File for application-wide exceptions"""


class CsvPocException(Exception):
    """Custom base exception class"""

    def __init__(self, message, data):
        super().__init__(message)
        self._message = message
        self._data = data

    @property
    def message(self):
        """User-friendly error message

        Returns:
            String representation of a user-friendly error message
        """
        return self._message

    @property
    def data(self):
        """Any data associated with a thrown exception

        Returns:
            Optional property that can contain any data related to the exception
            being thrown.
        """
        return self._data


class InvalidFileTypeException(CsvPocException):
    """Used when a POST request is made and the filetype is not supported"""

    pass


class InvalidMetadataException(CsvPocException):
    """Used when invalid query parameter values are sent in a request"""

    pass


class UnreadableFileException(CsvPocException):
    """Used when the API is unable to read an uploaded file"""

    pass


class DatabaseOpsException(CsvPocException):
    """Used when an unexpected database issue is hit"""

    pass


class FileNotFoundException(CsvPocException):
    """Used when a GET request is made with an ID that doesn't exist"""

    pass


class FilesystemException(CsvPocException):
    """Used when the server is unable to write to a local folder"""

    pass
