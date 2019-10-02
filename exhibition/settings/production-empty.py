from .default import *

SECRET_KEY = ''

DEBUG = False

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
