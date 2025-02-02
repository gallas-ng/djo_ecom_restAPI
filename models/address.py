from db import db


class AddressModel(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)

    store = db.relationship("StoreModel", back_populates="address")
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)