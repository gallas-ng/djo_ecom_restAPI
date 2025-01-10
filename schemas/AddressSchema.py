from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import db
from models import AddressModel

class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = AddressModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    street = fields.Str(required=True, validate=validate.Length(max=255))
    number = fields.Str(required=True, validate=validate.Length(max=5))
    city = fields.Str(required=True, validate=validate.Length(max=50))
    state = fields.Str(required=True, validate=validate.Length(max=50))
    longitude = fields.Float(allow_none=True)
    latitude = fields.Float(allow_none=True)

    store_id = fields.Int(dump_only=True)
    store = fields.Nested('StoreSchema', dump_only=True)
