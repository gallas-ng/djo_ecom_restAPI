from itertools import product

import cloudinary
import cloudinary.uploader
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from unicodedata import category

from db import db
from models import SubCategoryModel, StoreModel, ProductModel, CategoryModel
from schemas.ProductSchema import ProductSchema
from schemas.StoreSchema import StoreSchema
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


@blp.route('/store/<int:store_id>/product')
class StoreProductList(MethodView):
    @jwt_required()
    @blp.response(200, ProductSchema)
    def post(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        category = CategoryModel.query.get_or_404(int(request.form['category_id']))

        if category not in store.categories:
            store.categories.append(category)

        image_url = None
        if "image" in request.files:
            uploaded_file = request.files["image"]
            if uploaded_file:
                upload_result = cloudinary.uploader.upload(uploaded_file)
                image_url = upload_result.get("secure_url")
        else:
            abort(404, message='Please upload an image')


        product = ProductModel(
            label=request.form["label"],
            price_vat=request.form["price_vat"],
            price_ht=request.form["price_ht"],
            quantity=request.form["quantity"],
            description=request.form["description"],
            weight=request.form["weight"],
            image=image_url,
            ref=request.form["ref"],
            sub_category_id=request.form["sub_category_id"],
            store_id=store_id,
        )

        db.session.add(product)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the product", "details": str(e)}), 500

        return product

    @jwt_required()
    @blp.response(200, ProductSchema(many=True))
    def get(self, store_id):
        user_id = get_jwt_identity()
        store = StoreModel.query.get_or_404(store_id)
        if store.owner_id != int(user_id):
            abort(403, message='User and owner do not match.')

        return store.products


@blp.route('/store/<int:store_id>/product/<int:product_id>')
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    def put(self, store_id, product_id):
        store = StoreModel.query.get_or_404(store_id)
        product = ProductModel.query.get_or_404(product_id)
        category = CategoryModel.query.get_or_404(int(request.form['category_id']))

        if category not in store.categories:
            store.categories.append(category)

        image_url = None
        if "image" in request.files:
            uploaded_file = request.files["image"]
            if uploaded_file:
                upload_result = cloudinary.uploader.upload(uploaded_file)
                image_url = upload_result.get("secure_url")
        elif request.form['image'] == product.image:
            image_url = request.form['image']
        else:
            abort(404, message='Please upload an image')

        if request.form['label'] and request.form['price_vat'] and request.form['price_ht'] and request.form['quantity']:
            product.label = request.form['label']
            product.price_vat = request.form['price_vat']
            product.price_ht = request.form['price_ht']
            product.quantity = request.form['quantity']
            product.description = request.form['description']
            product.weight = request.form['weight']
            product.image = image_url
            product.ref = request.form['ref']
        else:
            abort(404, message= 'Fields are required.')

        db.session.add(product)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the product", "details": str(e)}), 500

        return product

    @jwt_required()
    @blp.response(202)
    def delete(self, store_id, product_id):
        store = StoreModel.query.get_or_404(store_id)
        product = ProductModel.query.get_or_404(product_id)

        product.delete()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while processing the product", "details": str(e)}), 500

        return {"message": "Product deleted."}
