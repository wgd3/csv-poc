"""Classes that can be used with SQLAlchemy models"""
import enum
import json
import datetime as dt

from csv_poc.extensions import db


class CRUDMixin(object):
    """Mixin with convenience methods for CRUD (create, read, update, delete)"""

    @classmethod
    def create(cls, save=True, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save(commit=save)

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

    def to_dict(self, show=None, hide=None, path=None, show_all=None):
        """Serialization method for any SQLAlchemy model

        This method was copy/pasted from a previous project, which was in turn
        copy/pasted/heavily modified from a StackOverflow post.

        Args:
            show: Column names to show
            hide: Column names to hide
            path: Period-delimited path to nested keys
            show_all: Toggle whether all fields are shown

        Returns:
            JSON representation of the model
        """
        if not show:
            show = []
        if not hide:
            hide = []
        hidden = []
        if hasattr(self, "hidden_fields"):
            hidden = self.hidden_fields
        default = []
        if hasattr(self, "default_fields"):
            default = self.default_fields

        ret_data = {}

        if not path:
            path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (path, item)
                return item

            show[:] = [prepend_path(x) for x in show]
            hide[:] = [prepend_path(x) for x in hide]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        for key in columns:
            check = "%s.%s" % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or key is "id" or check in show or key in default:
                val = getattr(self, key)
                if isinstance(val, (dt.datetime, dt.date)):
                    ret_data[key] = val.isoformat()
                elif isinstance(val, (enum.Enum,)):
                    ret_data[key] = val.value
                else:
                    ret_data[key] = getattr(self, key)

        for key in relationships:
            check = "%s.%s" % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    ret_data[key] = []
                    for item in getattr(self, key):
                        ret_data[key].append(
                            item.to_dict(
                                show=show,
                                hide=hide,
                                path=("%s.%s" % (path, key.lower())),
                                show_all=show_all,
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class
                        is not None
                    ):
                        ret_data[key] = getattr(self, key).to_dict(
                            show=show,
                            hide=hide,
                            path=("%s.%s" % (path, key.lower())),
                            show_all=show_all,
                        )
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            check = "%s.%s" % (path, key)
            if check in hide or key in hidden:
                continue
            if show_all or check in show or key in default:
                val = getattr(self, key)
                try:
                    ret_data[key] = json.loads(
                        json.dumps(val, cls=DateTimeEncoder)
                    )
                except:
                    pass

        return ret_data

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
