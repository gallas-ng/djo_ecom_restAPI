from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from db import db
from models import ProductModel, SubCategoryModel, StoreModel, OptionModel, FeedbackModel, \
    ProductOption  # Adjust import paths as needed

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = ProductModel
        # load_instance = True

    id = fields.Int(dump_only=True)
    label = fields.Str(required=True)
    price_vat = fields.Float(required=True)
    price_ht = fields.Float(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(allow_none=True)
    weight = fields.Float(allow_none=True)
    image = fields.Raw(allow_none=True)
    rating = fields.Float(allow_none=True)
    ref = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

    # Relationships
    sub_category_id = fields.Int(dump_only=True)
    sub_category = fields.Nested('SubCategorySchema', dump_only=True)  # Nested SubCategorySchema

    store_id = fields.Int(dump_only=True)
    store = fields.Nested('StoreSchema', dump_only=True)  # Nested StoreSchema

    options = fields.Nested('OptionSchema', many=True, dump_only=True)  # Nested OptionSchema for multiple options
    feedbacks = fields.Nested('FeedbackSchema', many=True, dump_only=True)  # Nested FeedbackSchema for multiple feedbacks


class ProductOptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductOption
        load_instance = True

    id = fields.Int(dump_only=True)
    product_id = fields.Int(dump_only=True)
    option_id = fields.Int(dump_only=True)

    # Relationships
    product = fields.Nested('ProductSchema', dump_only=True)  # Assuming you have a ProductSchema
    option = fields.Nested('OptionSchema', dump_only=True)  # Assuming you have an OptionSchema
