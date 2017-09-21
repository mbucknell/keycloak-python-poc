from flask import request
from flask_restplus import Api, Resource
from flask_jwt_simple import JWTManager, jwt_required
from flask_jwt_simple.exceptions import NoAuthorizationError

from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidAudienceError
from app import application
api = Api(application,
          title='Keycloak POC',
          default='Keycloak POC',
          default_label='Keycloak POC Endpoint',
          doc='/api')


# Setup the Flask-JWT-Simple extension
jwt = JWTManager(application)

# Adding all jwt exceptions that we care about to the api. Otherwise they all return a 500.
# The status returned for each error is determined by it's default error handler
# If we want to override the default status, we will need to override the default flask-jwt-simple
# functions using loader decorators
@api.errorhandler(ExpiredSignatureError) #Status 401
@api.errorhandler(NoAuthorizationError) #Status 401
@api.errorhandler(DecodeError) # Returns status 422
@api.errorhandler(InvalidAudienceError) # Status 422
def handler_invalid_token(error):
    return {'message': error.message}


@api.route('/endpoint')
class TestEndpoint(Resource):

    @jwt_required
    def get(self):
        return "Successful"