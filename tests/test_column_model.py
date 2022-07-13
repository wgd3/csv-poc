"""Main test suite for the Column database model"""
from sqlalchemy.exc import IntegrityError

from csv_poc.database.models import Column, File


class TestColumnModel:
    def setup_method(self):
        self.file = File.create(name="test_file.csv", path="test_path")

    def test_column_create(self, db):
        column = Column.create(
            file_id=self.file.id, col_index=1, col_name="test_column", col_type="text"
        )
        assert len(self.file.columns) == 1

    def test_non_nullable_index_constraint(self, db):
        try:
            column = Column.create(
                file_id=self.file.id,
                col_index=None,
                col_name="test_column",
                col_type="text",
            )
        except IntegrityError as ie:
            assert "columns.col_index" in str(ie)

    def test_non_nullable_name_constraint(self, db):
        try:
            column = Column.create(
                file_id=self.file.id,
                col_index=1,
                col_name=None,
                col_type="text",
            )
        except IntegrityError as ie:
            assert "columns.col_name" in str(ie)

    def test_non_nullable_file_id_constraint(self, db):
        try:
            column = Column.create(
                file_id=None,
                col_index=1,
                col_name="test_column",
                col_type="text",
            )
        except IntegrityError as ie:
            assert "columns.file_id" in str(ie)

    def test_col_type_enum_constraint(self, db):
        try:
            column = Column.create(
                file_id=self.file.id,
                col_index=1,
                col_name="test_column",
                col_type="blob",
            )
        except IntegrityError as ie:
            assert "columns.col_type" in str(ie)
