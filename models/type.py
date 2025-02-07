from db import db

class TypeModel(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(55), unique=True, nullable=False)
    code = db.Column(db.String(7), unique=True, nullable=False)

    #Relationship
    stores = db.relationship('StoreModel', back_populates='types', secondary='store_type')

    categories = db.relationship('CategoryModel', back_populates='type', lazy='dynamic', cascade='all, delete-orphan')

