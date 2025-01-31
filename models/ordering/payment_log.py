import datetime
from db import db


class PaymentLogModel(db.Model):
    __tablename__ = "payment_log"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)  # e.g., 'initiated', 'failed', 'completed'
    message = db.Column(db.String(255), nullable=True)  # Gateway response or error message
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    # Relationships
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    payment = db.relationship('PaymentModel', backref='logs', lazy=True)