"""Main test suite for the File database model"""
from sqlalchemy.exc import IntegrityError

from csv_poc.database.models import File


class TestFileModel:
    def test_file_create(self, db):
        file = File.create(name="test", path="test")
        assert file.name == "test"
        assert file.path == "test"
        assert len(file.columns) == 0

    def test_unique_name_constraint(self, db):
        name = "test name"
        first = File.create(name=name, path="test")
        try:
            second = File.create(name=name, path="second")
        except IntegrityError as ie:
            assert ie.params == (name, "second")
            assert "files.name" in str(ie)

    def test_unique_path_constraint(self, db):
        path = "test path"
        first = File.create(name="first", path=path)
        try:
            second = File.create(name="second", path=path)
        except IntegrityError as ie:
            assert ie.params == ("second", path)
            assert "files.path" in str(ie)

    def test_non_nullable_file_name(self, db):
        try:
            File.create(name=None, path="test")
        except IntegrityError as ie:
            assert "files.name" in str(ie)

    def test_non_nullable_file_path(self, db):
        try:
            File.create(name="test", path=None)
        except IntegrityError as ie:
            assert "files.path" in str(ie)

    def test_default_file_serialization(self, db):
        file = File.create(name="test", path="test")
        assert file.to_dict() == {
            "id": file.id,
            "name": file.name,
            # "path": file.path,
            # "columns": file.columns,
        }

    def test_added_fields_file_serialization(self, db):
        file = File.create(name="test", path="test")
        assert file.to_dict(show=["path", "columns"]) == {
            "id": file.id,
            "name": file.name,
            "path": file.path,
            "columns": file.columns,
        }
