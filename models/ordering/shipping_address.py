from email.policy import default

from db import db


class ShippingAddressModel(db.Model):
    __tablename__ = 'shipping_address'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    order = db.relationship('OrderModel', back_populates='shipping_address')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
