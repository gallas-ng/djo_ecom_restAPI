import os
import uuid

import cloudinary
import cloudinary.uploader
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import StoreModel, AddressModel
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
            store = StoreModel(id=store_id, title=store_data['title'], phone=store_data['phone'], image=image_url, address=address)
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