from .common import *  # noqa

import dj_database_url
import sys

DEBUG = False

ALLOWED_HOSTS = [
    'farafmb.de',
    'www.farafmb.de',
] + os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

ADMINS = [('Fachschaftsrat Maschinenbau', 'farafmb@ovgu.de')]


# Database

if len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }


# FileStorage

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = BASE_DIR / 'media'


# Security

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = False  # We're using nginx as reverse proxy

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
