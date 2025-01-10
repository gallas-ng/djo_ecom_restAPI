from itertools import product

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
    @blp.response(200, ProductSchema(many=True))
    def get(self, sub_category_id):
        sub_category = SubCategoryModel.query.get_or_404(sub_category_id)

        return sub_category.products.all()  # lazy="dynamic" means 'tags' is a query

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
