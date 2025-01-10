import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import StoreModel, AddressModel
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
        address = store.address
        # address = ?
        if store:
            store.title = store_data['title']
            store.phone = store_data['phone']
            store.image = store_data['image']
            store.address = address
        else:
            store = StoreModel(id=store_id, **store_data)
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
        store = StoreModel(
            title=store_data['title'],
            phone=store_data['phone'],
            image=store_data['image'],
            address=address,
        )
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(409, message='Store already exists')
        except SQLAlchemyError:
            abort(500, message="Something went wrong")

        return store
