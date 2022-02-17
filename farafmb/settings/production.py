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
