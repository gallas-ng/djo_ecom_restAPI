from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import TypeModel
from db import db

class TypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = TypeModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True, validate=validate.Length(max=55))
    code = fields.Str(required=True, validate=validate.Length(max=7))

    # stores = fields.List(fields.Nested('StoreSchema'), dump_only=True)
