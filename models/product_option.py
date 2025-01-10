from db import db

class ProductOption(db.Model):
    __tablename__ = 'product_option'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))