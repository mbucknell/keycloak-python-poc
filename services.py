
from flask_restplus import Api, Resource
from flask_restplus_jwt import JWTRestplusManager, jwt_required, jwt_role_required

from app import application


api = Api(application,
          title='Keycloak POC',
          default='Keycloak POC',
          default_label='Keycloak POC Endpoint',
          doc='/api')


# Setup the Flask-JWT-Simple extension
jwt = JWTRestplusManager(api, application)


@api.route('/endpoint')
class TestEndpoint(Resource):

    @api.header('Authorization', 'JWT token', required=True)
    @jwt_required
    def get(self):
        return "Successful"

@api.route('/role_endpoint')
class TestRoleProtectedEndPoint(Resource):

    @api.header('Authorization', 'JWT token', required=True)
    @jwt_role_required('admin')
    def get(self):
        return 'Successful'