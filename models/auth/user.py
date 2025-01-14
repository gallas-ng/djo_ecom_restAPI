import datetime
from tokenize import group

from sqlalchemy.orm import relationship

from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))


    isActive = db.Column(db.Boolean, default=True, nullable=False)
    isStaff = db.Column(db.Boolean, default=False, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
    isSuperAdmin = db.Column(db.Boolean, default=False, nullable=False)
    isSeller = db.Column(db.Boolean, default=False, nullable=False)
    isBuyer = db.Column(db.Boolean, default=False, nullable=False)

    groups = db.relationship('GroupModel', back_populates='users', secondary='user_group')

    feedbacks = db.relationship('FeedbackModel', back_populates='user', lazy='dynamic', cascade='all, delete')

    store = db.relationship('StoreModel', back_populates='owner', uselist=False)

    cart = db.relationship('CartModel', back_populates='user', uselist=False)

    orders = db.relationship('OrderModel', back_populates='user', cascade='all, delete')


