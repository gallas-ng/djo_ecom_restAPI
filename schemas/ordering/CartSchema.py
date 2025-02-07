from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import false

from models import CartModel


class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartModel
        # load_instance = True
        include_relationships = True

    session_id = fields.Str()
    user_id = fields.Integer(required=False)

    # Relationships
    items = fields.Nested('CartItemSchema', many=True)
