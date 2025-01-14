from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import OrderItemModel


class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItemModel
        # load_instance = True
        include_relationships = True

    order_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    subtotal = fields.Float(required=True)
