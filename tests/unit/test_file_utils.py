"""Unit tests for file utilities"""

from csv_poc.utils.file import guess_column_type, parse_columns
from csv_poc.database.models import File, Column


class TestGuessColumnType:
    def test_guess_date_success(self):
        test_date = "01/01/1989"
        assert guess_column_type(test_date) == "datetime"

    def test_guess_date_fail(self):
        assert guess_column_type(1928) != "datetime"

    def test_guess_number_success(self):
        assert guess_column_type(2022) == "number"

    def test_guess_text_success(self):
        assert guess_column_type("foobar") == "text"


class TestParseColumns:

    test_file_path = "/Users/wallace/git/csv-poc/tmp/uploads/Senior_Full_Stack_Developer_Assignment.csv"

    def setup(self):
        self.test_file = File.create(
            name="Senior_Full_Stack_Developer_Assignment.csv",
            path="/Users/wallace/git/csv-poc/tmp/uploads/Senior_Full_Stack_Developer_Assignment.csv",
        )

    def test_parse_columns(self, db):
        parse_columns(file_path=self.test_file_path, file_id=self.test_file.id)
        # make sure the new columns are placed in the session but not saved
        assert len(db.session.identity_map.values()) > 0
