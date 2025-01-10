import datetime

from sqlalchemy.dialects.postgresql import ARRAY

from db import db

class GroupModel(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    users = db.relationship('UserModel', back_populates='groups', secondary='user_group')