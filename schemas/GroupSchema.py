
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate

from db import db
from models import GroupModel, UserModel  # Adjust import paths as needed

class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        model = GroupModel
        # load_instance = True  # To load an instance of GroupModel
        include_relationships = True  # Include relationships in the schema

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=80))
    permissions = fields.Dict(allow_none=True)  # JSON field for permissions
    created_at = fields.DateTime(dump_only=True)

    # Nested relationships
    users = fields.List(fields.Nested('UserSchema', dump_only=True))  # Assuming you have a UserSchema
