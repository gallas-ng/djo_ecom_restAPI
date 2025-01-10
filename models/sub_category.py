import datetime

from db import db

class SubCategoryModel(db.Model):
    __tablename__ = 'sub_category'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('CategoryModel', back_populates='sub_categories')

    products = db.relationship('ProductModel', back_populates='sub_category', lazy='dynamic')
