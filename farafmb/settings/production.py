import os  # noqa
import re

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'www.farafmb.de',
    'farafmb.de',
]
if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))

PREPEND_WWW = True

ADMINS = [
    ('Fachschaftsrat Maschinenbau', 'farafmb@ovgu.de'),
]
if os.getenv('ADMINS'):
    ADMINS = [re.match(r'^([^<]+)\s<([^>]+)>$', admin).groups() for admin in os.getenv('ADMINS').splitlines()]


# Database

DATABASES = {
    'default': dj_database_url.config(),
}


# File storage

AWS_S3_ENDPOINT_URL = os.getenv('STORAGE_ENDPOINT_URL')

AWS_S3_ACCESS_KEY_ID = os.getenv('STORAGE_ACCESS_KEY')

AWS_S3_SECRET_ACCESS_KEY = os.getenv('STORAGE_SECRET_KEY')

# Upload static files via collectstatic to bucket
STATICFILES_STORAGE = 'farafmb.storage.StaticStorage'

STORAGE_STATIC_BUCKET = os.getenv('STORAGE_STATIC_BUCKET')

STORAGE_STATIC_DOMAIN = os.getenv('STORAGE_STATIC_DOMAIN', AWS_S3_ENDPOINT_URL)

STATIC_URL = f'https://{STORAGE_STATIC_DOMAIN}/'

# Upload media files to bucket
DEFAULT_FILE_STORAGE = 'farafmb.storage.MediaStorage'

STORAGE_MEDIA_BUCKET = os.getenv('STORAGE_MEDIA_BUCKET')

STORAGE_MEDIA_DOMAIN = os.getenv('STORAGE_MEDIA_DOMAIN', AWS_S3_ENDPOINT_URL)

MEDIA_URL = f'https://{STORAGE_MEDIA_DOMAIN}/'

# Default ACL on file. Otherwise, inheriting bucket ACL
AWS_DEFAULT_ACL = 'public-read'


# Email

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL', 'no-reply@farafmb.de')

SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'no-reply@farafmb.de')


# Security

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 3600  # TODO Increase to 1 year (365*24*60*60)

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
