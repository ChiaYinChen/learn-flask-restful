from flask_jwt import jwt_required
from flask_restful import Resource

from ..common import utils
from ..model.user import User as UserModel


class User(Resource):

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.parser = utils.user_parser()

    def get(self, username):
        """Get user detail information."""
        user = UserModel.get_by_username(username)
        if user:
            return user.as_dict()
        return {'message': 'User not found.'}, 404

    def post(self, username):
        """Create a user."""
        data = self.parser.parse_args()
        user = UserModel.get_by_username(username)
        if user:
            return {'message': 'User already exist.'}
        user = UserModel(
            username=username,
            email=data['email']
        )
        user.set_password(data['password'])
        user.add()
        return {
            'message': 'Insert user success.',
            'user': user.as_dict()
        }, 201

    def delete(self, username):
        """Delete user."""
        user = UserModel.get_by_username(username)
        if user:
            user.delete()
            return {'message': 'User deleted.'}
        else:
            return {'message': 'User not found.'}, 404

    def put(self, username):
        """Update user."""
        user = UserModel.get_by_username(username)
        if user:
            data = self.parser.parse_args()
            user.password_hash = data['password']
            user.update()
            return {
                'message': 'Update user success.',
                'user': user.as_dict()
            }
        else:
            return {'message': 'User not found.'}, 404


class UserList(Resource):

    @jwt_required()
    def get(self):
        """Get user list."""
        users = UserModel.get_all_user()
        return [user.as_dict() for user in users]
