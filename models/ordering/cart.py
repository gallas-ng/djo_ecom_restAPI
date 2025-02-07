import datetime

from db import db
from models.ordering.cart_item import CartItemModel


class CartModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now)
    session_id = db.Column(db.String(255), nullable=True, unique=True)

    # Relationship
    user = db.relationship('UserModel', back_populates='cart')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    items = db.relationship('CartItemModel', back_populates='cart', cascade='all, delete')

    def add_item(self, product_id, quantity, price_vat):
        item = next((i for i in self.items if i.product_id == product_id), None)
        if item:
            if item.quantity == 0 and quantity < 0:
                quantity = 0
            item.quantity += quantity
        else:
            new_item = CartItemModel(product_id=product_id, quantity=quantity, price=price_vat, cart_id=self.id)
            db.session.add(new_item)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'items': [item.to_dict() for item in self.items],  # Assuming items also have `to_dict`
        }