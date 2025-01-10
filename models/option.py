import enum

from db import db

class OptionTypeEnum(enum.Enum):
    color = 'color'
    size = 'size'

class ColorArrayEnum(enum.Enum):
    black = 'black'
    white = 'white'

class SizeArrayEnum(enum.Enum):
    large = 'large'
    small = 'small'

class OptionModel(db.Model):
    __tablename__ = 'option'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=True)
    typeArray = db.Column(db.String(80), nullable=True)

    products = db.relationship('ProductModel', back_populates='options', secondary='product_option')

