import datetime

from db import db

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    address = db.relationship('AddressModel', back_populates='store', uselist=False)

    types = db.relationship('TypeModel', back_populates='stores', secondary='store_type')
    categories = db.relationship('CategoryModel', back_populates='stores', secondary='store_category')

    products = db.relationship('ProductModel', back_populates='store', lazy='dynamic', cascade='all, delete')

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('UserModel', back_populates='store')
    #owner = user