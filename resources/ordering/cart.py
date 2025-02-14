import uuid


from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from models import CartModel, CartItemModel, ProductModel
from db import db
from schemas.ordering.CartSchema import CartSchema
from schemas.ordering.CartItemSchema import CartItemSchema

blp = Blueprint("Cart", __name__, description="Operations on the shopping cart")


@blp.route("/cart")
class CartView(MethodView):
    # Unused -------------------------------------------
    @jwt_required(optional=True)
    @blp.response(200)
    def get(self):
        """Retrieve the cart for logged-in or guest users."""
        user_id = get_jwt_identity()  # Check if user is logged in
        session_id = request.headers.get('Session-ID')

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            print(session_id)
            cart = CartModel.query.filter_by(session_id=session_id).first()
        else:
            return {"message": "Cart not found.", "session_id": str(uuid.uuid4())}, 404

        return cart
    #---------------------------------------------------


    @jwt_required(optional=True)
    # @blp.arguments(CartSchema) -- Since we changed the response body Marshmallow
    # is no longer used for this method
    @blp.response(201)
    def post(self):
        """
        Create or find a user's cart based on the session_id or user_id
        :return:
        """
        session_id = request.cookies.get('session_id')
        user_id = None

        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except Exception as e:
            # Keep User_id None when a jwt error is raised
            pass

        cart = None

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
            if not cart:
                cart = CartModel(user_id=user_id)
                db.session.add(cart)
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()
            if not cart:
                cart = CartModel(session_id=session_id)
                db.session.add(cart)
        else:
            session_id = str(uuid.uuid4())
            cart = CartModel(session_id=session_id)
            db.session.add(cart)

        db.session.commit()

        response = make_response(jsonify({"message": "Cart created or fetched", "cart": cart.to_dict()}))

        if not request.cookies.get('session_id'):
            response.set_cookie('session_id', session_id, httponly=True, max_age=3600 * 24 * 7)

        return response


@blp.route("/cart/item")
class CartItemView(MethodView):
    @jwt_required(optional=True)
    # @blp.arguments(CartItemSchema) -- Since we changed the response body Marshmallow
    # is no longer used for this method
    @blp.response(201)
    def post(self):
        """Add an item to the cart or update the cart item"""
        user_id = get_jwt_identity()
        session_id = request.cookies.get('session_id')

        if not user_id and not session_id:
            abort(400, message="No user or session ID found")

        cart = None
        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()

        if not cart:
            abort(400, message="Cart not found")

        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        price_vat = data.get('price_vat')

        if not product_id:
            abort(400, message="Product ID is required")

        cart.add_item(product_id, quantity, price_vat)
        db.session.commit()

        return jsonify({"message": "Item added", "cart": cart.to_dict()})

    @jwt_required(optional=True)
    def put(self):
        """Remove an item from the cart."""
        user_id = get_jwt_identity()
        session_id = request.cookies.get('session_id')
        cart = None

        if user_id:
            cart = CartModel.query.filter_by(user_id=user_id).first()
        elif session_id:
            cart = CartModel.query.filter_by(session_id=session_id).first()

        if not cart:
            abort(404, message="Cart not found")

        data = request.get_json()
        product_id = data.get('product_id')

        cart_item = next((item for item in cart.items if item.product_id == product_id), None)
        if not cart_item:
            return {"message": "Item not found in cart."}, 404

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item deleted", "cart": cart.to_dict()})
