from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import db
from models import OptionModel

class OptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = OptionModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True, validate=validate.Length(max=80))
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)  # Assumes OptionTypeEnum is handled as a string
    typeArray = fields.Str(allow_none=True)  # Assumes TypeArrayEnum is handled as a string

    products = fields.List(fields.Nested('ProductSchema'), dump_only=True)

