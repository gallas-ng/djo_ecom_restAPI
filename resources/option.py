import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import OptionModel, ProductModel
from schemas.OptionSchema import OptionSchema
from schemas.ProductSchema import ProductSchema, ProductOptionSchema

blp = Blueprint('Options', __name__, description="Operations on options")

@blp.route('/option/<string:option_id>')
class Option(MethodView):
    @blp.response(200, OptionSchema) # *1 What should be returned ?
    def get(self, option_id):
        option = OptionModel.query.get_or_404(id=option_id)
        return option

    @blp.arguments(OptionSchema)
    @blp.response(200, OptionSchema)
    def put(self, option_data, option_id):
        # option_data = request.get_json()
        option = OptionModel.query.get(id=option_id)
        if option:
            option.label = option_data['label']
            option.description = option_data['description']
            option.type = option_data['type']
            option.typeArray = option_data['typeArray']
        else:
            option = OptionModel(id=option_id, **option_data)
        db.session.add(option)
        db.session.commit()

        return option

    @jwt_required()
    def delete(self, option_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")

        option = OptionModel.query.get_or_404(id=option_id)
        db.session.delete(option)
        db.session.commit()
        return {"message": "type deleted"}

@blp.route('/option')
class OptionList(MethodView):
    # @jwt_required()
    @blp.response(200, OptionSchema(many=True))
    def get(self):
        return OptionModel.query.all()

    @blp.arguments(OptionSchema)
    @blp.response(201, OptionSchema)
    def post(self, option_data):
        option = OptionModel(**option_data)
        try:
            db.session.add(option)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong")
        return option

@blp.route("/product/<string:product_id>/option/<string:option_id>")
class LinkOptionToProduct(MethodView):
    @blp.response(201, ProductOptionSchema)
    def post(self, product_id, option_id):
        product = ProductModel.query.get_or_404(product_id)
        option = OptionModel.query.get_or_404(option_id)

        product.options.append(option)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the option.")

        return option

    @blp.response(200, ProductOptionSchema)
    def delete(self, product_id, option_id):
        product = ProductModel.query.get_or_404(product_id)
        option = OptionModel.query.get_or_404(option_id)

        product.options.remove(option)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the option.")

        return {"message": "Product removed from Option", "store": product, "option": option}


