"""Database model for tracking column data in CSV files"""
from ..mixins import PkModel
from csv_poc.extensions import db


class Column(PkModel):
    """Column model represents a single column in a given CSV file

    `Column` has a many-to-one relationship with the `files` table.
    """

    __tablename__ = "columns"
    col_index = db.Column(db.Integer, nullable=False)
    col_name = db.Column(db.String, nullable=False)
    col_type = db.Column(
        db.Enum("text", "number", "datetime", name="column_type_enum"),
        default="text",
        nullable=False,
    )
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"), nullable=False)

    def __repr__(self):
        return f"<Column {self.col_name} has type {self.col_type}"
