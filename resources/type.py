import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import TypeModel, StoreModel
from schemas.TypeSchema import TypeSchema
from schemas.StoreSchema import StoreTypeSchema, StoreSchema, StoreCategorySchemaInc

blp = Blueprint('Types', __name__, description="Operations on types")

@blp.route('/type/<string:type_id>')
class Type(MethodView):
    @blp.response(200, TypeSchema) # *1 What should be returned ?
    def get(self, type_id):
        """
        Get a type
        :param type_id:
        :return:
        """
        type = TypeModel.query.get_or_404(id=type_id)
        return type

    @blp.arguments(TypeSchema)
    @blp.response(200, TypeSchema)
    def put(self, type_data, type_id):
        """
        Update a type
        :param type_data:
        :param type_id:
        :return:
        """
        # type_data = request.get_json()
        type = TypeModel.query.get(id=type_id)
        if type:
            type.label = type_data['label']
            type.code = type_data['code']
        else:
            type = TypeModel(id=type_id, **type_data)
        db.session.add(type)
        db.session.commit()

        return type

    @jwt_required()
    def delete(self, type_id):
        """
        Update a type
        :param type_id:
        :return:
        """
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")

        type = TypeModel.query.get_or_404(id=type_id)
        db.session.delete(type)
        db.session.commit()
        return {"message": "type deleted"}

@blp.route('/type')
class TypeList(MethodView):
    # @jwt_required()
    @blp.response(200, TypeSchema(many=True))
    def get(self):
        """
        Get All types
        :return:
        """
        return TypeModel.query.all()

    @blp.arguments(TypeSchema)
    @blp.response(201, TypeSchema)
    def post(self, type_data):
        """Add a type"""
        type = TypeModel(**type_data)
        try:
            db.session.add(type)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong")
        return type


@blp.route("/store/<string:store_id>/type/<string:type_id>")
class LinkTypeToStore(MethodView):
    """
    Handling many to many relationship between stores and types
    """
    @blp.response(201, StoreTypeSchema)
    def post(self, store_id, type_id):
        store = StoreModel.query.get_or_404(store_id)
        type = TypeModel.query.get_or_404(type_id)

        store.types.append(type)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the type.")

        return type

    @blp.response(200, StoreTypeSchema)
    def delete(self, store_id, type_id):
        store = StoreModel.query.get_or_404(store_id)
        type = TypeModel.query.get_or_404(type_id)

        store.types.remove(type)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the type.")

        return {"message": "Store removed from Type", "store": store, "type": type}


@blp.route('/type/<int:type_id>/stores')
class StoresByType(MethodView):
    @blp.response(200, StoreCategorySchemaInc(many=True))
    def get(self, type_id):
        """
        Get the stores for a type
        :param type_id:
        :return:
        """
        type = TypeModel.query.get_or_404(type_id)
        return type.stores
