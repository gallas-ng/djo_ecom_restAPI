from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import db
from models import SubCategoryModel


class SubCategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = SubCategoryModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

    category_id = fields.Int(dump_only=True)
    # category = fields.Nested('CategorySchema', dump_only=True)
    # products = fields.List(fields.Nested('ProductSchema'), dump_only=True)

class SubCatProductsSchema(SubCategorySchema):
    products = fields.List(fields.Nested('ProductSchema'), dump_only=True)