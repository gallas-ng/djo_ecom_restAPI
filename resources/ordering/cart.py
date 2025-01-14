import uuid
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import CartModel, CartItemModel, ProductModel
from db import db
from schemas.ordering.CartSchema import CartSchema
from schemas.ordering.CartItemSchema import CartItemSchema

blp = Blueprint("Cart", __name__, description="Operations on the shopping cart")


@blp.route("/cart")
class CartView(MethodView):
    @blp.response( 200,CartSchema)
    def get(self):
        """Retrieve the cart for logged-in or guest users."""
        user_id = get_jwt_identity()  # Check if user is logged in
        session_id = request.cookies.get('session_id')  # Retrieve session ID for guests

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()
        else:
            return {"message": "Cart not found."}, 404

        return cart

    @blp.arguments(CartSchema)
    @blp.response( 201,CartSchema)
    def post(self):
        """Create or retrieve a cart for logged-in or guest users."""
        user_id = get_jwt_identity()
        session_id = request.cookies.get('session_id')

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
            if not cart:
                cart = CartModel(user_id=user_id)
                db.session.add(cart)
        else:
            if not session_id:
                # Generate a new session ID for the guest user
                session_id = str(uuid.uuid4())
                response = make_response({"message": "Guest cart created."}, 201)
                response.set_cookie('session_id', session_id)
            cart = CartModel.query.filter_by(session_id=session_id).first()
            if not cart:
                cart = CartModel(session_id=session_id)
                db.session.add(cart)

        db.session.commit()
        return cart


@blp.route("/cart/item")
class CartItemView(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(CartItemSchema)
    @blp.response( 201,CartItemSchema)
    def post(self):
        """Add an item to the cart."""
        user_id = get_jwt_identity()
        session_id = request.cookies.get('session_id')
        cart = None

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()

        if not cart:
            return {"message": "Cart not found."}, 404

        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Validate product
        product = ProductModel.query.get(product_id)
        if not product:
            return {"message": "Product not found."}, 404

        # Add or update item in cart
        cart_item = next((item for item in cart.items if item.product_id == product_id), None)
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItemModel(cart=cart, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        return cart_item

    @jwt_required(optional=True)
    def delete(self):
        """Remove an item from the cart."""
        user_id = get_jwt_identity()
        session_id = request.cookies.get('session_id')
        cart = None

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()

        if not cart:
            return {"message": "Cart not found."}, 404

        data = request.get_json()
        product_id = data.get('product_id')

        cart_item = next((item for item in cart.items if item.product_id == product_id), None)
        if not cart_item:
            return {"message": "Item not found in cart."}, 404

        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Item removed from cart."}, 200
