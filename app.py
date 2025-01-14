import os
from flask import Flask, jsonify
from flask_admin.theme import Bootstrap4Theme
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from dotenv import load_dotenv
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from admin_views.CategoryAdminView import CategoryAdminView
from admin_views.FeedbackAdminView import FeedbackAdminView
from admin_views.GroupAdminView import GroupAdminView
from admin_views.OptionViewModel import OptionAdminView
from admin_views.ProductAdminView import ProductAdminView
from admin_views.StoreAdminView import StoreAdminView
from admin_views.SubCategoryAdminView import SubCategoryAdminView
from admin_views.TypeAdminView import TypeAdminView
from admin_views.UserAdminView import UserAdminView

from blocklist import BLOCKLIST
from db import db
from models import *

from resources.auth.user import blp as UserBlueprint
from resources.auth.group import blp as GroupBlueprint
from resources.type import blp as TypeBlueprint
from resources.option import blp as OptionBlueprint
from resources.product import blp as ProductBlueprint
from resources.store import blp as StoreBlueprint
from resources.feedback import blp as FeedbackBlueprint, Feedback
from resources.sub_category import blp as SubCategoryBlueprint
from resources.category import blp as CategoryBlueprint
from resources.ordering.cart import blp as CarrtBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    load_dotenv()

    app.secret_key = os.getenv("SECRET_KEY")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Djo E-Commerce Rest API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-secret-key")

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {"description": "Request does not contain an access token.", "error": "authorization_required"}
        ), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401

    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(GroupBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(TypeBlueprint)
    api.register_blueprint(OptionBlueprint)
    api.register_blueprint(SubCategoryBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(FeedbackBlueprint)
    api.register_blueprint(CarrtBlueprint)

    admin = Admin(app, name='Djo E-commerce Panel', theme=Bootstrap4Theme(swatch='lux'))
    admin.add_view(UserAdminView(UserModel, db.session, category='Auth'))
    admin.add_view(GroupAdminView(GroupModel, db.session, category='Auth'))
    admin.add_view(TypeAdminView(TypeModel, db.session, category='Item'))
    admin.add_view(StoreAdminView(StoreModel, db.session))
    admin.add_view(CategoryAdminView(CategoryModel, db.session, category='Countable'))
    admin.add_view(SubCategoryAdminView(SubCategoryModel, db.session, category='Countable'))
    admin.add_view(ProductAdminView(ProductModel, db.session, category='Item'))
    admin.add_view(OptionAdminView(OptionModel, db.session, category='Item'))
    admin.add_view(FeedbackAdminView(FeedbackModel, db.session, category='Item'))


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
