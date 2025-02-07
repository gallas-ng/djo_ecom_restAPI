from db import db


class OrderItemModel(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)  # quantity * price

    #Relationship
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('OrderModel', back_populates='items')

    product = db.relationship('ProductModel')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
