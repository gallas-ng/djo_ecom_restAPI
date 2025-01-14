import datetime

from db import db

class OrderModel(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # e.g., 'pending', 'shipped'
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now)

    user = db.relationship('UserModel', back_populates='orders')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    items = db.relationship('OrderItemModel', back_populates='order', cascade='all, delete-orphan')

    shipping_address = db.relationship('ShippingAddressModel', back_populates='order', uselist=False)
