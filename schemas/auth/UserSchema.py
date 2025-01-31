from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from sqlalchemy import false

from db import db
from models import UserModel, UserGroup  # Adjust import paths as needed

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = UserModel
        # load_instance = True  # To load a UserModel instance
        include_relationships = True  # Ensures relationships are included

    id = fields.Int(dump_only=True)
    username = fields.Str(required=False, validate=validate.Length(max=80))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True)  # You might want to handle password securely
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    google_id = fields.Str(allow_none=True)

    isActive = fields.Bool(default=True)
    isStaff = fields.Bool(default=False)
    isAdmin = fields.Bool(default=False)
    isSuperAdmin = fields.Bool(default=False)
    isSeller = fields.Bool(default=False)
    isBuyer = fields.Bool(default=False)

    # Relationships
    groups = fields.List(fields.Nested('GroupSchema'), dump_only=True)  # Assuming you have a GroupSchema
    feedbacks = fields.List(fields.Nested('FeedbackSchema'), dump_only=True)  # Assuming you have a FeedbackSchema
    store = fields.Nested('StoreSchema', dump_only=True)  # Assuming you have a StoreSchema
    cart = fields.Nested('CartSchema', allow_none=True)
    orders = fields.Nested('OrderSchema', many=True)

class UserGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserGroup
        load_instance = True  # To load an instance of UserGroup
        include_relationships = True  # Include relationships in the schema

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    group_id = fields.Int(dump_only=True)

    # Relationships
    user = fields.Nested('UserSchema', dump_only=True)  # Assuming you have a UserSchema
    group = fields.Nested('GroupSchema', dump_only=True)  # Assuming you have a GroupSchema
