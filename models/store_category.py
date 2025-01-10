from db import db

class StoreCategory(db.Model):
    __tablename__ = 'store_category'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
