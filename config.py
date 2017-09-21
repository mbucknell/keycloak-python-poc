import os

DEBUG = False
JWT_ALGORITHM = 'RS256'
JWT_PUBLIC_KEY = os.environ.get('JWT_PUBLIC_KEY', '')

JWT_DECODE_AUDIENCE = os.environ.get('JWT_DECODE_AUDIENCE', 'security-admin-console')
