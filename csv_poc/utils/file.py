"""Utilities related to examining and parsing CSV files"""
from flask import current_app
import csv
import re

from csv_poc.database.models import Column


def guess_column_type(content) -> str:
    """Attempts to parse the type of content within a given column

    Starts by attempting to match a date regex. If that fails, check to see if
    the content is purely numbers. If both checks fail, assume the content is
    just plain text.

    TODO This does NOT account for `NoneType` or other primitives

    Args:
        content: String or number

    Returns:
        One of "text", "number", or "datetime"
    """
    current_app.logger.debug(
        f"Attempting to parse type of content for input: {content}"
    )
    match = re.search(r"(\d+/\d+/\d+)", content)
    if match:
        current_app.logger.debug(
            f"Input appears to be a date, matched pattern '(\d+/\d+/\d+)'"
        )
        return "datetime"

    match = re.search(r"^\d+$", content)
    if match or isinstance(content, int):
        current_app.logger.debug(
            f"Input appears to be a number, matched pattern '^\d+$'"
        )
        return "number"

    current_app.logger.debug(
        "Checks for datetime and number failed, assuming plain text"
    )
    # this is rather lazy, but if the prior checks fail then this is the only
    # other option
    return "text"


def parse_columns(file_path: str, file_id: int):
    """Examine columns in a CSV file and create Column objects

    Args:
        file_path: String with path to CSV file to open
        file_id: Primary key for the File instance to associate the column with

    Returns:
        A list of Column instances that have been created and added to the
        database session but HAVE NOT been commited yet.
    """
    try:
        with open(file_path, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = list(csv_reader)

            # extract header row and the first data row
            header_row: str = rows[0]
            content_row: str = rows[1] if len(rows) > 1 else None
            # current_app.logger.debug(f"Header row:\n{header_row}")
            # current_app.logger.debug(f"Content row:\n{content_row}")

            # split the header row into individual columns
            # column_names = header_row.split(",")

            # use `enumerate` here to access the index
            for idx, name in enumerate(header_row):
                # current_app.logger.debug(
                #     f"Evaluating column {idx} named '{name}'"
                # )
                if content_row:
                    column_content = content_row[idx]
                    col_type = guess_column_type(content=column_content)
                    # current_app.logger.debug(
                    #     f"Set column '{name}' to type '{col_type}'"
                    # )

                # finally, create a new Column instance but do not save at this
                # time
                Column.create(
                    save=False,
                    col_index=idx,
                    col_name=name,
                    col_type=col_type,
                    file_id=file_id,
                )

    except Exception as e:
        current_app.logger.error(
            f"Unknown error occurred while parsing columns:\n{str(e)}"
        )
