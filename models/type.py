from db import db

class TypeModel(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(55), unique=True, nullable=False)
    code = db.Column(db.String(7), unique=True, nullable=False)

    stores = db.relationship('StoreModel', back_populates='types', secondary='store_type')

