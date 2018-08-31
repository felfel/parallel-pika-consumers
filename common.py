from extensions import db

from guid import GUID

db.GUID = GUID


# ### DB Models ###
class DBEditMixin(object):
    last_edited_at = db.Column(db.DateTime, nullable=False, onupdate=db.func.now(), default=db.func.now()) # TODO: Should this be set by db?
    last_edited_by = db.Column(db.GUID, nullable=False)


class DBCreateMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.GUID, nullable=False)
