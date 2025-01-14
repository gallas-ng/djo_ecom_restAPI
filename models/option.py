import enum

from db import db


class OptionModel(db.Model):
    __tablename__ = 'option'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(80), nullable=False)

    products = db.relationship('ProductModel', back_populates='options', secondary='product_option')

