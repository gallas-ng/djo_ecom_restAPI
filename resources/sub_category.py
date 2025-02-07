from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import SubCategoryModel, CategoryModel, StoreModel
from schemas.ProductSchema import ProductSchema
from schemas.SubCategorySchema import SubCategorySchema, SubCatProductsSchema

blp = Blueprint("Sub_categories", __name__, description="Operations on sub_categories")


@blp.route('/category/<string:category_id>/sub_category')
class SubCategoryAdd(MethodView):
    @blp.arguments(SubCategorySchema)
    @blp.response(201, SubCategorySchema)
    def post(self, sub_category_data, category_id):
        """
        Add a new sub_category.
        :param sub_category_data:
        :param category_id:
        :return:
        """
        if SubCategoryModel.query.filter(SubCategoryModel.category_id == category_id,
                                         SubCategoryModel.label == sub_category_data["label"]).first():
            abort(400, message="A sub_category with that name already exists in that category.")

        sub_category = SubCategoryModel(**sub_category_data, category_id=category_id)

        try:
            db.session.add(sub_category)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return sub_category

@blp.route("/sub_category/<string:sub_category_id>")
class SubCategory(MethodView):
    @blp.response(200, SubCategorySchema)
    def get(self, sub_category_id):
        """
        Get a sub_category.
        :param sub_category_id:
        :return:
        """
        sub_category = SubCategoryModel.query.get_or_404(sub_category_id)
        return sub_category

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, sub_category_id):
        """
        Delete a sub_category.
        :param sub_category_id:
        :return:
        """
        sub_category = SubCategoryModel.query.get_or_404(sub_category_id)
        try:
            db.session.delete(sub_category)
            db.session.commit()
            return {"message": "Sub Category deleted."}
        except SQLAlchemyError as e:
            abort(
                400,
                message="Could not delete sub_category. Make sure sub_category is not associated with any items, then try again.",  # noqa: E501
            )

@blp.route("/sub_category/<string:sub_category_id>/products")
class ProductList(MethodView):
    @blp.response(200, SubCatProductsSchema(many=True))
    def get(self, sub_category_id):
        """
        Get all products for a sub_category.
        :param sub_category_id:
        :return:
        """
        sub_category = SubCategoryModel.query.get_or_404(sub_category_id)

        return sub_category.products.all()

@blp.route("/store/<int:store_id>/sub_category/<int:sub_category_id>/products")
class StoreSubCatProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))  # Utilisez le schéma approprié pour vos produits
    def get(self, store_id, sub_category_id):
        """
        Get all products for a store by sub_category.
        """
        store = StoreModel.query.get_or_404(store_id)
        sub_category = SubCategoryModel.query.get_or_404(sub_category_id)

        products = sub_category.products.filter_by(store_id=store_id).all()

        return products