import datetime
from db import db


class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    stores = db.relationship('StoreModel', back_populates='categories', secondary='store_category')

    sub_categories = db.relationship('SubCategoryModel', back_populates='category', lazy="dynamic", cascade="all, delete")