import datetime

from db import db

class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), unique=False, nullable=False)
    price_vat = db.Column(db.Float, unique=False, nullable=False)
    price_ht = db.Column(db.Float, unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    weight = db.Column(db.Float, unique=False, nullable=True)
    image = db.Column(db.LargeBinary, unique=False, nullable=True)
    rating = db.Column(db.Float, unique=False, nullable=True)
    ref = db.Column(db.String(100), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))


    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'), nullable=True)
    sub_category = db.relationship('SubCategoryModel', back_populates='products')

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)
    store = db.relationship('StoreModel', back_populates='products')

    options = db.relationship('OptionModel', back_populates='products', secondary='product_option')


    feedbacks = db.relationship('FeedbackModel', back_populates='product', lazy='dynamic', cascade='all, delete')

