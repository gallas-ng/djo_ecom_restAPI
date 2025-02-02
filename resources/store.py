import json
import os
import uuid

import cloudinary
import cloudinary.uploader
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import StoreModel, AddressModel, TypeModel, UserModel
from schemas.CategorySchema import CategorySchema
from schemas.StoreSchema import StoreSchema
from schemas.AddressSchema import AddressSchema

blp = Blueprint('Stores', __name__, description="Operations on stores")


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        image_file = request.files.get('image')
        image_url = None
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']

        address = store.address
        # address = ?
        if store:
            store.title = store_data['title']
            store.phone = store_data['phone']
            store.image = image_url
            store.address = address
        else:
            store = StoreModel(id=store_id, title=store_data['title'], phone=store_data['phone'], image=image_url,
                               address=address)
        db.session.add(store)
        db.session.commit()

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        address = AddressModel(**store_data['address'])
        image_file = request.files.get('image')
        image_url = None
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']
        store = StoreModel(
            title=store_data['title'],
            phone=store_data['phone'],
            image=image_url,
            address=address,
            owner=store_data['owner']
        )
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(409, message='Store already exists')
        except SQLAlchemyError:
            abort(500, message="Something went wrong")

        return store


@blp.route('/store/<int:store_id>/categories')
class CategoriesByStore(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.categories


@blp.route('/user/store/<int:user_id>')
class SellerStore(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, user_id):
        store = StoreModel.query.filter_by(owner_id=user_id).first()

        if not store:
            abort(404, message='Store not found')

        return store


@blp.route('/seller/store')
class SellerStoreAdd(MethodView):
    @jwt_required()
    @blp.response(201, StoreSchema)
    def post(self):
        user_id = get_jwt_identity()
        types = request.form['types']
        types = json.loads(types)

        if store := StoreModel.query.filter_by(owner_id=user_id).first():
            abort(409, message='User already has one store')

        # user = UserModel.query.get_or_404(user_id)

        address = AddressModel(
            street=request.form['street'],
            number=request.form['number'],
            # district=request.form['district'],
            city=request.form['city'],
            state=request.form['state'],
        )
        db.session.add(address)
        db.session.flush()

        image_url = None
        if "image" in request.files:
            uploaded_file = request.files["image"]
            if uploaded_file:
                # Envoyer l'image sur Cloudinary
                upload_result = cloudinary.uploader.upload(uploaded_file)
                image_url = upload_result.get("secure_url")  # URL sécurisée de l'image


        store = StoreModel(
            title=request.form['title'],
            phone=request.form['phone'],
            image=image_url,
            address=address,
            owner_id=user_id
        )

        db.session.add(store)
        db.session.flush()

        address.store_id = store.id

        print(types)
        # selected_types = TypeModel.query.filter(TypeModel.id.in_(types)).all()
        for tid in types:
            type = TypeModel.query.get_or_404(int(tid))
            store.types.append(type)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the order", "details": str(e)}), 500

        return store

@blp.route('/seller/store/<int:store_id>')
class SellerStoreEdit(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        user_id = get_jwt_identity()
        types = request.form['types']
        types_id = json.loads(types)

        if store:
            if user_id != store.owner_id:
                abort(403, message='You are not the owner of the store')

        address = None
        if store.address:
            address = store.address
        else:
            address = AddressModel(
                street=request.form['street'],
                number=request.form['number'],
                # district=request.form['district'],
                city=request.form['city'],
                state=request.form['state'],
            )
            db.session.add(address)
            db.session.flush()

        image_url = None
        if "image" in request.files:
            uploaded_file = request.files["image"]
            if uploaded_file:
                upload_result = cloudinary.uploader.upload(uploaded_file)
                image_url = upload_result.get("secure_url")
        else:
            abort(404, message='Please upload a logo')

        if request.form['title'] and request.form['phone']:
            store.title=request.form['title']
            store.phone=request.form['phone']
            store.image=image_url
            store.address=address

            db.session.add(store)
            db.session.flush()
        else:
            abort(404, message='No title and phone are specified')


        address.store_id = store.id

        for tid in types_id:
            type = TypeModel.query.get_or_404(int(tid))
            if type not in store.types:
                store.types.append(type)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the order", "details": str(e)}), 500

        return store




