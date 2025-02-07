import hashlib
import time

from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import CartModel, OrderModel, ShippingAddressModel, CartItemModel, OrderItemModel, PaymentModel, \
    PaymentLogModel
from db import db

blp = Blueprint("Payment", __name__, description="Operations payments")


@blp.route('/checkout')
class Checkout(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self):
        """
        Process to order payment
        :return:
        """
        user_id = get_jwt_identity()
        data = request.json

        if not data.get("order_id") or not data.get("payment_method"):
            abort(400, message="Missing required fields")

        order_id = data["order_id"]
        amount = data["amount"]
        payment_method = data["payment_method"]

        # Combine order_id, payment_method, and a timestamp
        raw_string = f"{order_id}-{payment_method}-{int(time.time() * 1000)}"
        # Generate a hash and truncate it to 9 characters
        transaction_id = hashlib.sha256(raw_string.encode()).hexdigest()[:9]

        order = OrderModel.query.filter_by(id=order_id).first()
        if not order:
            abort(404, message="Invalid order ID")

        if order.total_amount != amount:
            abort(400, message="Payment amount does not match order total")

        payment = PaymentModel(
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
        )
        db.session.add(payment)

        try:
            db.session.commit()
            # Simulate online payment gateway processing (e.g., PayPal)
            if payment_method != "cash":
                payment.status = "completed"  # Simulate a successful payment
                db.session.commit()
            return jsonify({"message": "Payment processed successfully", "payment_id": payment.id, "transaction_id": transaction_id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the payment", "details": str(e)}), 500
