from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import TypeModel
from db import db
from schemas.CategorySchema import CategorySchema


class TypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = TypeModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True, validate=validate.Length(max=55))
    code = fields.Str(required=True, validate=validate.Length(max=7))

    categories = fields.Nested('CategorySchema', many=True, dump_only=True)
    # stores = fields.List(fields.Nested('StoreSchema'), dump_only=True)
