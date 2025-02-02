from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from db import db
from models import StoreModel, StoreType, AddressModel, TypeModel, CategoryModel, ProductModel, UserModel, StoreCategory


class StoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = StoreModel
        # load_instance = True  # Pour charger directement une instance de StoreModel
        include_relationships = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=80))
    phone = fields.Str(validate=validate.Length(max=80))
    image = fields.Str()
    created_at = fields.DateTime(dump_only=True)

    address = fields.Nested('AddressSchema', allow_none=True)
    owner_id = fields.Int()

    # Nested relationships
    types = fields.List(fields.Nested('TypeSchema'), dump_only=True)
    # categories = fields.List(fields.Nested('CategorySchema'), dump_only=True)
    # products = fields.List(fields.Nested('ProductSchema'), dump_only=True)
    #
    # owner = fields.Nested('UserSchema', dump_only=True)


class StoreTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StoreType
        load_instance = True

    id = fields.Int(dump_only=True)
    type_id = fields.Int(required=True)
    store_id = fields.Int(required=True)

    type = fields.Nested('TypeSchema', dump_only=True)
    store = fields.Nested('StoreSchema', dump_only=True)

class StoreCategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StoreCategory
        load_instance = True

    id = fields.Int(dump_only=True)
    category_id = fields.Int(dump_only=True)
    store_id = fields.Int(dump_only=True)

    # Relationships
    category = fields.Nested('CategorySchema', dump_only=True)  # Nested CategorySchema
    store = fields.Nested('StoreSchema', dump_only=True)  # Nested StoreSchema

class StoreCategorySchemaInc(StoreSchema):
    categories = fields.List(fields.Nested('CategorySchema'), dump_only=True)

class StoreProductSchemaInc(StoreSchema):
    products = fields.List(fields.Nested('ProductSchema'), dump_only=True)
