from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import CartItemModel


class CartItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartItemModel
        # load_instance = True
        include_relationships = True

    cart_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
