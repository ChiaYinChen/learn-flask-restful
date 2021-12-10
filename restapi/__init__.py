"""Create and configure the app."""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
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

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Flask Restful Project',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
    })
    docs = FlaskApiSpec(app)

    api.add_resource(Helloworld, '/')
    api.add_resource(User, '/user/<string:username>')
    api.add_resource(UserList, '/users')
    api.add_resource(Tweet, '/tweet/<string:username>')
    docs.register(User)
    docs.register(UserList)
    docs.register(Tweet)
    return app
