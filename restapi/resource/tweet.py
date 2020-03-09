from flask_jwt import current_identity, jwt_required
from flask_restful import Resource

from ..common import utils
from ..model.tweet import Tweet as TweetModel
from ..model.user import User as UserModel


class Tweet(Resource):

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.parser = utils.tweet_parser()

    @jwt_required()
    def post(self, username):
        """Create a tweet by username."""
        if current_identity.username != username:
            return {'message': 'Please use the right token.'}
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'User not found.'}, 404
        data = self.parser.parse_args()
        tweet = TweetModel(
            body=data['body'],
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
