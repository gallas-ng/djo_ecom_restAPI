from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import SubCategoryModel, StoreModel, CategoryModel, ProductModel, FeedbackModel
from schemas.FeedbackSchema import FeedbackSchema

blp = Blueprint("Feedbacks", __name__, description="Operations on feedbacks")


@blp.route("/product/<string:product_id>/feedback")
class ProductFeedback(MethodView):
    @blp.response(200, FeedbackSchema(many=True))
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)

        return product.feedbacks.all()  # lazy="dynamic" means 'tags' is a query

    @blp.arguments(FeedbackSchema)
    @blp.response(201, FeedbackSchema)
    def post(self, feedback_data, product_id):
        if SubCategoryModel.query.filter(FeedbackModel.product_id == product_id, FeedbackModel.id == feedback_data["id"]).first():
            abort(400, message="A feedback with that name already exists in that product.")

        feedback = SubCategoryModel(**feedback_data, product_id=product_id)

        try:
            db.session.add(feedback)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return feedback



@blp.route("/feedback/<string:feedback_id>")
class Feedback(MethodView):
    @blp.response(200, FeedbackSchema)
    def get(self, feedback_id):
        feedback = FeedbackModel.query.get_or_404(feedback_id)
        return feedback


    def delete(self, feedback_id):
        feedback = FeedbackModel.query.get_or_404(feedback_id)
        try:
            db.session.delete(feedback)
            db.session.commit()
            return {"message": "Feedback deleted."}
        except SQLAlchemyError as e:
            abort(
                400,
                message="Could not delete feedback.",  # noqa: E501
            )