"""Create and configure the app."""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_restful import Api
from webargs.core import DEFAULT_VALIDATION_STATUS
from webargs.flaskparser import abort, parser

from .common.connection import db
from .config import app_config
from .model.user import User as UserModel
from .resource.hello import Helloworld
from .resource.tweet import Tweet
from .resource.user import User, UserList

migrate = Migrate()
jwt = JWT(None, UserModel.authenticate, UserModel.identity)


# ref: https://github.com/marshmallow-code/webargs/issues/181
# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(
    err, req, schema, *, error_status_code, error_headers
):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    status_code = error_status_code or DEFAULT_VALIDATION_STATUS
    abort(
        status_code,
        exc=err,
        messages=err.messages,
    )


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
    docs.register(Helloworld)
    docs.register(User)
    docs.register(UserList)
    docs.register(Tweet)
    return app
