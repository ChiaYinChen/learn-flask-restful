"""Create and configure the app."""
from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_restful import Api

from .common.connection import db
from .config import app_config
from .model.user import User as UserModel
from .resource.hello import Helloworld
from .resource.tweet import Tweet
from .resource.user import User, UserList

migrate = Migrate()
jwt = JWT(None, UserModel.authenticate, UserModel.identity)


def create_app(config_name='development'):

    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api.add_resource(Helloworld, '/')
    api.add_resource(User, '/user/<string:username>')
    api.add_resource(UserList, '/users')
    api.add_resource(Tweet, '/tweet/<string:username>')
    return app
