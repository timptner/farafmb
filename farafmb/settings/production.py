import os

from .base import *

# Debug
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Security
SECURE_HSTS_SECONDS = 3600  # TODO set value to 31536000 when tested properly
SECURE_SSL_REDIRECT = False  # nginx already redirects to https
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
