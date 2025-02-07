import datetime
import enum

from db import db

class natureEnum(enum.Enum):
    NS = 'Not Satisfied'
    S = 'Satisfied'
    N = 'None'


class FeedbackModel(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    nature = db.Column(db.Enum(natureEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    #Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('UserModel', back_populates='feedbacks')

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('ProductModel', back_populates='feedbacks')