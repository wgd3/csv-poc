"""Database model for tracking uploaded CSV files"""
from ..mixins import PkModel
from csv_poc.extensions import db


class File(PkModel):
    """File model saves basic information about a given CSV file"""

    __tablename__ = "files"
    name = db.Column(db.String, nullable=False, unique=True)
    path = db.Column(db.String, nullable=False, unique=True)
    columns = db.relationship("Column", backref="file", lazy=True)

    def __repr__(self):
        return f"<File '{self.name}'>"

    def to_json(self):
        """Serialization method for the model

        Returns:
            Valid JSON object
        """
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "columns": self.columns,
        }
