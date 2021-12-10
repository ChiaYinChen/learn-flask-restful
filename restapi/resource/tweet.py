from flask_apispec import doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource

from ..model.tweet import Tweet as TweetModel
from ..model.user import User as UserModel
from ..schema.tweet import TweetCreate


@doc(
    tags=['Tweet'],
    params={
        'Authorization': {
            'description': 'Authorization: Bearer <access_token>',
            'in': 'header',
            'type': 'string',
            'required': True
        }
    }
)
class Tweet(MethodResource, Resource):

    @use_kwargs(TweetCreate, location=('json'))
    @jwt_required()
    def post(self, username, **kwargs):
        """Create a tweet by username."""
        if current_identity.username != username:
            return {'message': 'Please use the right token.'}
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'User not found.'}, 404
        tweet = TweetModel(
            body=kwargs.get('body'),
            user_id=user.id
        )
        tweet.add()
        return {
            'message': 'Post success.',
            'tweet': tweet.as_dict()
        }, 201

    @jwt_required()
    def get(self, username):
        """Get a user tweet list."""
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'User not found.'}, 404
        return [t.as_dict() for t in user.tweet]
