from .default import *

import os


# You need to generate a secret key
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = ''

DEBUG = False

# Needed for when running behind a proxy
USE_X_FORWARDED_HOST = True

# Replace with your DNS name
ALLOWED_HOSTS = ['cometonotos.hps.gr']

# Where the static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Keep these and use HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Settings for sending emails
EMAIL_HOST = 'mail.hps.gr'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@hps.gr'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Configure and fill in whatever authentication methods
# you will use - in addition to local passwords
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

# Exhibition details and settings
EXHIBITION_NAME = 'NOTOS 2021'
EXHIBITION_URL = 'http://hps.gr/notos2021/'
EXHIBITION_EMAIL = 'notos2021@hps.gr'
EXHIBITION_LOGO = 'notos_2021.jpg'

# Communication language in addition to English
NATIVE_COMMUNICATION_LANGUAGE = ('EL', 'Greek')

# Authorization key to register appointments
APPOINTMENTS_AUTHORIZATION_KEY = 'KEY'

# Hide exhibit entry forms
ENTRY_FORMS_HIDDEN = False

# Whenever a new commissioner or juror is registered, we email the
# president of the respective federation. Whenever a new exhibitor
# is registered, we email the commissioner of the exhibitors country.
# If we have no commissioner contact, we email to this address (if it exists).
NO_COMMISSIONER_EMAIL = ''

# We note to emails sent to commissioners that any objections should
# be directed to this email.
GENERAL_COMMISSIONER_EMAIL = ''

# Add these recipients to any emails sent.
EMAIL_ADDITIONAL_RECIPIENTS = []

# Send all emails only to the additional recipients list
EMAIL_ONLY_ADDITIONAL_RECIPIENTS = False
