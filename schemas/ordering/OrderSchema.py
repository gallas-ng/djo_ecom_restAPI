from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import OrderModel


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        # load_instance = True
        include_relationships = True

    user_id = fields.Integer(required=True)
    total_amount = fields.Float(required=True)
    status = fields.String(required=True)
    items = fields.Nested('OrderItemSchema', many=True)
    shipping_address = fields.Nested('ShippingAddressSchema')
