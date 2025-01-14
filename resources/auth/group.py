from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint

from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import GroupModel, UserModel
from schemas.auth.GroupSchema import GroupSchema
from schemas.auth.UserSchema import UserGroupSchema

blp = Blueprint('Groups', __name__, description="Operations on groups")

@blp.route('/group/<string:group_id>')
class Group(MethodView):
    @blp.response(200, GroupSchema) # *1 What should be returned ?
    def get(self, group_id):
        group = GroupModel.query.get_or_404(id=group_id)
        return group

    @blp.arguments(GroupSchema)
    @blp.response(200, GroupSchema)
    def put(self, group_data, group_id):
        # group_data = request.get_json()
        group = GroupModel.query.get(id=group_id)
        if group:
            group.name = group_data['name']
            group.permissions = group_data['permissions']
        else:
            group = GroupModel(id=group_id, **group_data)
        db.session.add(group)
        db.session.commit()

        return group

    @jwt_required()
    def delete(self, group_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")

        group = GroupModel.query.get_or_404(id=group_id)
        db.session.delete(group)
        db.session.commit()
        return {"message": "type deleted"}

@blp.route('/group')
class GroupList(MethodView):
    # @jwt_required()
    @blp.response(200, GroupSchema(many=True))
    def get(self):
        return GroupModel.query.all()

    @blp.arguments(GroupSchema)
    @blp.response(201, GroupSchema)
    def post(self, group_data):
        group = GroupModel(**group_data)
        try:
            db.session.add(group)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong")
        return group

@blp.route("/user/<string:user_id>/group/<string:groupe_id>")
class LinkGroupToUser(MethodView):
    @blp.response(201, UserGroupSchema)
    def post(self, user_id, group_id):
        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)

        user.groups.append(group)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the group.")

        return group

    @blp.response(200, UserGroupSchema)
    def delete(self, user_id, group_id):
        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)

        user.groups.remove(group)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the group.")

        return {"message": "Store removed from Type", "user": user, "group": group}


