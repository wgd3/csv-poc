"""Unit tests for the Files DAO"""
from sqlite3 import OperationalError, IntegrityError

from werkzeug.datastructures import FileStorage

from csv_poc.database.models import File
from csv_poc.api.v1.files_dao import FileDAO
import mock
import os

from csv_poc.utils.exc import DatabaseOpsException, InvalidFileTypeException


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, "..", os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


class TestListFiles:
    def setup(self):
        for i in range(5):
            File.create(
                name=f"testfile{i}.csv", path=f"/path/to/testfile{i}.csv"
            )

    def test_list_all_files(self, db):
        files = FileDAO.list_files()
        assert len(files) == 5

    @mock.patch(
        "csv_poc.database.models.File.query.all", side_effect=OperationalError()
    )
    def test_list_files_ops_error(self, db):
        try:
            FileDAO.list_files()
        except DatabaseOpsException as dbe:
            assert dbe.data is None


class TestAddFile:
    def test_invalid_extension(self):
        file_storage = FileStorage(filename="bad.file")
        try:
            FileDAO.add_file(file_storage=file_storage)
        except InvalidFileTypeException as invalid:
            assert invalid.data is None

    def test_integrity_error(self):
        File.create(name="foo.csv", path="bar")
        file_storage = FileStorage(filename="foo.csv")
        try:
            FileDAO.add_file(file_storage=file_storage)
        except DatabaseOpsException as dbe:
            assert dbe.message == "File already exists"

    def test_add_success(self):
        file_path = os.path.join(PROJECT_ROOT, "sample.csv")
        with open(file_path, "rb") as file:
            file_storage = FileStorage(file)
            file = FileDAO.add_file(file_storage=file_storage)
            assert "sample.csv" in file["name"]
