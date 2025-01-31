from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import db
from models import CategoryModel

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = CategoryModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

    # stores = fields.List(fields.Nested('StoreSchema'), dump_only=True)
    # sub_categories = fields.List(fields.Nested('SubCategorySchema'), dump_only=True)

class CategorySubSchema(CategorySchema):
    sub_categories = fields.List(fields.Nested('SubCategorySchema'), dump_only=True)
