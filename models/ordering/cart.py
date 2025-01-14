import datetime

from db import db

class CartModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now)
    session_id = db.Column(db.String(255), nullable=True, unique=True)

    user = db.relationship('UserModel', back_populates='cart')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    items = db.relationship('CartItemModel', back_populates='cart', cascade='all, delete')
