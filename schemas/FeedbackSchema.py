from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import db
from models import FeedbackModel

class FeedbackSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = FeedbackModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    message = fields.Str(allow_none=True)
    nature = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    user_id = fields.Int(dump_only=True)
    # user = fields.Nested('UserSchema', dump_only=True)
    product_id = fields.Int(dump_only=True)
    # product = fields.Nested('ProductSchema', dump_only=True)

