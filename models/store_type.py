from db import db

class StoreType(db.Model):
    __tablename__ = 'store_type'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))