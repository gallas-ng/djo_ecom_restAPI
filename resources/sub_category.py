from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import SubCategoryModel, CategoryModel
from schemas.SubCategorySchema import SubCategorySchema

blp = Blueprint("Sub_categories", __name__, description="Operations on sub_categories")


@blp.route("/category/<string:category_id>/sub_category")
class SubCatInCategory(MethodView):
    @blp.response(200, SubCategorySchema(many=True))
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)

        return category.sub_categories.all()  # lazy="dynamic" means 'tags' is a query

    @blp.arguments(SubCategorySchema)
    @blp.response(201, SubCategorySchema)
    def post(self, sub_category_data, category_id):
        if SubCategoryModel.query.filter(SubCategoryModel.category_id == category_id, SubCategoryModel.label == sub_category_data["label"]).first():
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