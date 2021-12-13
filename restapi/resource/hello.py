from flask_apispec import doc
from flask_apispec.views import MethodResource
from flask_restful import Resource


@doc(tags=['Home'], description='Hello world')
class Helloworld(MethodResource, Resource):

    def get(self):
        return 'Hello world'
