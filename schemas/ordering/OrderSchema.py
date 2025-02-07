from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import OrderModel


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        # load_instance = True
        include_relationships = True

    total_amount = fields.Float(required=True)
    status = fields.String(required=True)
    shipping_mode = fields.Integer(required=True)

    # Relationships
    shipping_address = fields.Nested('ShippingAddressSchema')
    items = fields.Nested('OrderItemSchema', many=True)
    user_id = fields.Integer(required=True)
