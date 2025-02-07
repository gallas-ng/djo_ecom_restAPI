from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import OrderItemModel
from schemas.ProductSchema import ProductSchema


class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItemModel
        # load_instance = True
        include_relationships = True

    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    subtotal = fields.Float(required=True)

    # Relationships
    product_id = fields.Integer(required=True)
    product = fields.Nested(ProductSchema)

    order_id = fields.Integer(required=True)
