import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import CategoryModel, StoreModel, StoreCategory, SubCategoryModel
from schemas.CategorySchema import CategorySchema, CategorySubSchema
from schemas.SubCategorySchema import SubCategorySchema
from schemas.StoreSchema import StoreCategorySchema

blp = Blueprint('Categories', __name__, description="Operations on categories")

@blp.route('/category/<string:category_id>')
class Category(MethodView):
    @blp.response(200, CategorySchema) # *1 What should be returned ?
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(id=category_id)
        return category

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def put(self, category_data, category_id):
        category = CategoryModel.query.get(id=category_id)
        if category:
            category.label = category_data['label']
            category.description = category_data['description']
        else:
            category = CategoryModel(id=category_id, **category_data)
        db.session.add(category)
        db.session.commit()

        return category

    @jwt_required()
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(id=category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}

@blp.route('/category')
class Category(MethodView):
    # @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong")
        return category

@blp.route("/store/<string:store_id>/category/<string:category_id>")
class LinkCategoriesToStore(MethodView):
    @blp.response(201, StoreCategorySchema)
    def post(self, store_id, category_id):
        store = StoreModel.query.get_or_404(store_id)
        category = CategoryModel.query.get_or_404(category_id)

        store.categories.append(category)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category

    @blp.response(200, StoreCategorySchema)
    def delete(self, store_id, category_id):
        store = StoreModel.query.get_or_404(store_id)
        category = CategoryModel.query.get_or_404(category_id)

        store.categories.remove(category)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return {"message": "Store removed from Type", "store": store, "type": type}


@blp.route("/category/<string:category_id>/sub_categories")
class SubCatInCategory(MethodView):
    @blp.response(200, CategorySubSchema(many=True))
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        sub_categories_with_products = category.sub_categories.filter(SubCategoryModel.products.any()).all()

        return sub_categories_with_products

@blp.route("/store/<string:store_id>/types/categories")
class CategoriesInStore(MethodView):
    @blp.response(200, CategorySubSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        categories = [category for type in store.types for category in type.categories]

        return categories



