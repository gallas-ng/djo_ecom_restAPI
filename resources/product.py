from itertools import product

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import SubCategoryModel, StoreModel, ProductModel
from schemas.ProductSchema import ProductSchema
from schemas.SubCategorySchema import SubCategorySchema

blp = Blueprint("Products", __name__, description="Operations on products")


@blp.route("/sub_category/<string:sub_category_id>/product")
class ProductList(MethodView):
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data, sub_category_id):
        if ProductModel.query.filter(ProductModel.sub_category_id == sub_category_id, ProductModel.id == product_data["id"]).first():
            abort(400, message="A product with that id already exists in that category.")

        product = ProductModel(
            **product_data,
            sub_category_id=sub_category_id,
        )

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return product



@blp.route("/product/<string:product_id>")
class Product(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    @blp.response(
        202,
        description="Deletes a product if no item is tagged with it.",
        example={"message": "Product deleted."},
    )
    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Sub Category deleted."}
        except SQLAlchemyError as e:
            abort(
                400,
                message="Could not delete product. Make sure product is not associated with any sub cats, then try again.",  # noqa: E501
            )

@blp.route('/product/rate/upd')
class ProductRate(MethodView):
    @blp.response(200)
    def put(self):
        data = request.get_json()
        product = ProductModel.query.get_or_404(data["product_id"])

        if not product:
            abort(400, message="Product does not exist.")

        product.rating = data["rate"]
        db.session.add(product)
        db.session.commit()

        return "Product updated."

