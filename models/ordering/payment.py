import datetime
from db import db

class PaymentModel(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)  # Total amount paid
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., 'cash', 'paypal', 'wave'
    transaction_id = db.Column(db.String(100), nullable=True)  # For online payments (optional for cash)
    status = db.Column(db.String(20), nullable=False, default="pending")  # 'pending', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.UTC))

    # Relationships
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('OrderModel', back_populates='payment')

