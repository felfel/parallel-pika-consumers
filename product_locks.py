

# ### DB models ###
import uuid

from marshmallow import fields

from guid import GUID
from extensions import db, ma
from common import DBEditMixin, DBCreateMixin

db.GUID = GUID


class ProductLock(DBCreateMixin, DBEditMixin, db.Model):
    id = db.Column(db.GUID(), primary_key=True, default=uuid.uuid4)
    warehouse_id = db.Column(db.GUID(), nullable=False)
    operator_id = db.Column(db.GUID(), nullable=False)
    product_id = db.Column(db.GUID(), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)


# ### SCHEMAS ###
class ProductLockSchema(ma.ModelSchema):
    class Meta:
        model = ProductLock

    created_by = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_edited_by = fields.UUID(dump_only=True)
    last_edited_at = fields.DateTime(dump_only=True)

    # constraints
    __table_args__ = (db.UniqueConstraint('warehouse_id', 'product_id', 'released_at'))
