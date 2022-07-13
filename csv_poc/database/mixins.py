"""Classes that can be used with SQLAlchemy models"""
from csv_poc.extensions import db


class CRUDMixin(object):
    """Mixin with convenience methods for CRUD (create, read, update, delete)"""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() if commit else self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class PkModel(CRUDMixin, db.Model):
    """Base SQLAlchemy model class

    This abstract class includes an integer-type primary key column, as well
    as the CRUD operations from `CRUDMixin`. Intended to be used as the base
    for any database models and save some repeated code.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None
