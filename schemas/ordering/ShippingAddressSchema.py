from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import ShippingAddressModel


class ShippingAddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingAddressModel
        # load_instance = True

    order_id = fields.Integer(required=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    phone = fields.String(required=True)
    postal_code = fields.String(required=True)
    country = fields.String(required=True)
