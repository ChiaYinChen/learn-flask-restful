from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt import jwt_required
from flask_restful import Resource

from ..model.user import User as UserModel
from ..schema.user import User as UserOutput
from ..schema.user import UserCreate


@doc(tags=['User'])
@marshal_with(UserOutput)
class User(MethodResource, Resource):

    def get(self, username):
        """Get user detail information."""
        user = UserModel.get_by_username(username)
        if user:
            return user
        return make_response({'message': 'User not found.'}, 404)

    @use_kwargs(UserCreate, location=('json'))
    def post(self, username, **kwargs):
        """Create a user."""
        user = UserModel.get_by_username(username)
        if user:
            return make_response({'message': 'User already exist.'}, 200)
        user = UserModel(
            username=username,
            email=kwargs.get('email')
        )
        user.set_password(kwargs.get('password'))
        user.add()
        return user, 201

    def delete(self, username):
        """Delete user."""
        user = UserModel.get_by_username(username)
        if user:
            user.delete()
            return make_response({'message': 'User deleted.'}, 200)
        else:
            return make_response({'message': 'User not found.'}, 404)

    @use_kwargs(UserCreate, location=('json'))
    def put(self, username, **kwargs):
        """Update user."""
        user = UserModel.get_by_username(username)
        if user:
            user.set_password(kwargs.get('password'))
            user.update()
            return user
        else:
            return make_response({'message': 'User not found.'}, 404)


class UserList(Resource):

    @jwt_required()
    def get(self):
        """Get user list."""
        users = UserModel.get_all_user()
        return [user.as_dict() for user in users]
