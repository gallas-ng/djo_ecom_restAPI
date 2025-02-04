import uuid
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

from models import CartModel, OrderModel, ShippingAddressModel, CartItemModel, OrderItemModel, ProductModel, UserModel
from db import db

blp = Blueprint("Order", __name__, description="Operations on the orders")


@blp.route('/order')
class Order(MethodView):
    @jwt_required()
    @blp.response(201)
    def post(self):
        user_id = get_jwt_identity()  # Retrieve the user ID from the JWT (if logged in)
        data = request.json

        # Validate input
        if not data.get("cart_id") or not data.get("total_price") or data.get("shipping_method") is None:
            abort(404, message="Missing required fields")

        cart_id = data["cart_id"]
        total_price = data["total_price"]
        shipping_method = data["shipping_method"]
        shipping_address = data.get("shipping_address")  # May be None for onsite

        # Retrieve the cart and its items
        cart_items = CartItemModel.query.filter_by(cart_id=cart_id).all()
        if not cart_items:
            abort(404, message="Invalid cart or empty cart")

        # Validate shipping address for delivery mode
        if shipping_method != 0 and not shipping_address:
            abort(400, message="Shipping address is required for delivery")

        # If shipping_method is delivery, validate and store the shipping address
        address = None
        if shipping_method != 0:
            address = ShippingAddressModel(
                street=shipping_address.get("street"),
                city=shipping_address.get("city"),
                postal_code=shipping_address.get("postalcode"),
                country=shipping_address.get("country"),
                phone=shipping_address.get("phone"),
            )
            db.session.add(address)
            db.session.flush()  # This allows us to retrieve the address ID before commit

        # Create the order
        order = OrderModel(
            total_amount=total_price,
            shipping_mode=shipping_method,
            shipping_address=address,
            user_id=user_id,
        )
        db.session.add(order)
        db.session.flush()  # Retrieve order ID for creating order items

        if address is not None:
            address.order_id = order.order_id

        # Create OrderItemModel entries from CartItemModel
        order_items = []
        for cart_item in cart_items:
            order_item = OrderItemModel(
                product_id=cart_item.product_id,
                order_id=order.id,
                quantity=cart_item.quantity,
                price=cart_item.price,
                subtotal=cart_item.quantity * cart_item.price,  # Calculate subtotal
            )
            order_items.append(order_item)

        # Add all order items to the session
        db.session.add_all(order_items)

        # Clear the cart after creating the order
        CartItemModel.query.filter_by(cart_id=cart_id).delete()  # Remove cart items

        # Commit changes
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the order", "details": str(e)}), 500

        return jsonify({"message": "Order created successfully", "order_id": order.id}), 201


@blp.route('/order/<string:order_id>')
class OrderUpdate(MethodView):
    @jwt_required()
    @blp.response(204)
    def put(self, order_id):
        user_id = get_jwt_identity()
        data = request.json()

        order = OrderModel.query.filter_by(order_id=order_id).first()
        if not order:
            abort(404, message="Order not found")

        order.status = data.get("status")

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the order", "details": str(e)}), 500

        return jsonify({"message": "Order updated successfully", "order_id": order.id}), 201




@blp.route('/store/<int:store_id>/orders')
class PurchaseHistoryResource(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self, store_id):
        """Store products purchase history"""
        user_id = get_jwt_identity()

        purchases = (
            db.session.query(
                ProductModel.label.label("product_name"),
                ProductModel.rating.label("rate"),
                OrderItemModel.quantity,
                (OrderItemModel.price * OrderItemModel.quantity).label("subtotal"),
                OrderModel.created_at.label("purchase_date"),
                UserModel.username.label("user")
            )
            .join(OrderItemModel, ProductModel.id == OrderItemModel.product_id)
            .join(OrderModel, OrderItemModel.order_id == OrderModel.id)
            .join(UserModel, OrderModel.user_id == UserModel.id)
            .filter(ProductModel.store_id == store_id)
            .all()
        )

        if not purchases:
            return {"message": "Aucun achat trouvé pour ce magasin"}, 404


        purchases_data = [
            {
                "product_name": p.product_name,
                "quantity": p.quantity,
                "subtotal": p.subtotal,
                "purchase_date": p.purchase_date.strftime("%Y-%m-%d %H:%M:%S"),
                "user": p.user,
                "rate": p.rate
            }
            for p in purchases
        ]

        return {"purchases": purchases_data}