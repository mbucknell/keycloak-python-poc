import os

DEBUG = False
JWT_ALGORITHM = 'HS256'
JWT_PUBLIC_KEY = os.environ.get('JWT_PUBLIC_KEY', '')
JWT_SECRET_KEY = 'secret'

#JWT_DECODE_AUDIENCE = os.environ.get('JWT_DECODE_AUDIENCE', 'security-admin-console')

def get_role (dict):
    return dict['role']
JWT_ROLE_CLAIM = get_role
JWT_ROLE = 'admin'
