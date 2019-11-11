from .default import *

import os

SECRET_KEY = ''

DEBUG = False

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['cometonotos.hps.gr']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

APPOINTMENTS_AUTHORIZATION_KEY = 'KEY'
