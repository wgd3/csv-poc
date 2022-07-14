"""Database model for tracking uploaded CSV files"""
from ..mixins import PkModel
from csv_poc.extensions import db


class File(PkModel):
    """File model saves basic information about a given CSV file"""

    # default keys returned when serializing an instance
    default_fields = ["id", "name"]

    __tablename__ = "files"
    name = db.Column(db.String, nullable=False, unique=True)
    path = db.Column(db.String, nullable=False, unique=True)
    columns = db.relationship("Column", backref="file", lazy=True)

    def __repr__(self):
        return f"<File '{self.name}'>"
