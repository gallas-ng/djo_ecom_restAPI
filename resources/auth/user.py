import os

from flask import request
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_

from google.oauth2 import id_token
from google.auth.transport import requests

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from models import OrderModel
from resources.ordering.order import Order
from schemas.auth.UserSchema import UserSchema
from schemas.ordering.OrderSchema import OrderSchema
from schemas.ordering.OrderItemSchema import OrderItemSchema
from schemas.ordering.ShippingAddressSchema import ShippingAddressSchema

blp = Blueprint("Users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"],
                )
        ).first()
        if user :
            abort(409, message="A user with that username or email already exists.")


        user = UserModel(
            username=user_data['username'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data["password"]),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            phone=user_data.get('phone'),
            isSeller=user_data.get('isSeller')
        )
        db.session.add(user)
        db.session.commit()

        # send_user_registration_email(user.email, user.username)

        return {"message": "User created successfully.", "user": user.to_dict()}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            expires = 1*24*60
            return {"access_token": access_token, "refresh_token": refresh_token, "user": user.to_dict(), "expires": expires}, 200

        abort(401, message="Invalid credentials.")


@blp.route('/google-login')
class GoogleLogin(MethodView):
    def post(self):
        data = request.get_json()
        token = data.get('token')
        isSeller = data.get('isSeller')

        try:
            # Vérifier le token Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
            print(idinfo)

            email = idinfo['email']
            name = idinfo.get('name')
            google_id = idinfo['sub']
            first_name = idinfo.get('given_name')
            last_name = idinfo.get('family_name')
            phone = idinfo.get('phone_number')
            password = pbkdf2_sha256.hash(str(google_id))

            user = UserModel.query.filter_by(email=email).first()
            if not user:
                # Créer un utilisateur s'il n'existe pas
                user = UserModel(email=email, username=name, password=password, google_id=google_id, first_name=first_name, last_name=last_name, phone=phone, isSeller=isSeller)
                db.session.add(user)
                db.session.commit()

            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            expires = 1*24*60
            return {'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict(), 'expires': expires}, 200

        except ValueError:
            abort(400, message="Token Google invalide.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@blp.route('/user/<int:user_id>/pwd')
class UserSecret(MethodView):
    @jwt_required()
    def put(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        data = request.get_json()
        password = data.get('password')
        new_password = data.get('new_password')
        if not user:
            abort(401, message="User not found.")
        if pbkdf2_sha256.verify(password, user.password):
            user.password = pbkdf2_sha256.hash(new_password)
            db.session.add(user)
            db.session.commit()
        else :
            abort(401, message="Invalid credentials.")

        return {"message": "Password updated successfully.", "user": user.to_dict()}, 200

@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        db.session.add(user)
        db.session.commit()

        return {"message": "User updated.", "user": user.to_dict()}, 200

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        new_token = create_access_token(identity=str(current_user), fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        # jti = get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/user/<int:user_id>/orders")
class UserDetails(MethodView):
    # @jwt_required()
    @blp.response(200, OrderSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        if not user:
            abort(404, message="User not found.")

        orders = user.orders

        return orders
