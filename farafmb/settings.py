import dj_database_url
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'farafmb.de',
    'www.farafmb.de',
]

ADMINS = [
    ('Fachschaftsrat Maschinenbau', 'farafmb@ovgu.de'),
]


# Application definition

INSTALLED_APPS = [
    'about',
    'blog',
    'excursions',
    'jobs',
    'meetings',
    'members',
    'office_hours',

    'django.contrib.admin',
    'django.contrib.auth',

    'mozilla_django_oidc',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'mozilla_django_oidc.middleware.SessionRefresh',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'farafmb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'farafmb' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'markdown': 'farafmb.templatetags.markdown',
            },
        },
    },
]

WSGI_APPLICATION = 'farafmb.wsgi.application'


# Database

DATABASES = {
    'default': dj_database_url.config(),
}


# Authentication

AUTHENTICATION_BACKENDS = [
    'farafmb.auth.CustomOIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID')

OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET')

OIDC_RP_SIGN_ALGO = 'RS256'

OIDC_OP_JWKS_ENDPOINT = 'https://auth.faking.cool/.well-known/jwks.json'

OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://auth.faking.cool/oauth2/authorize'

OIDC_OP_TOKEN_ENDPOINT = 'https://auth.faking.cool/oauth2/token'

OIDC_OP_USER_ENDPOINT = 'https://auth.faking.cool/oauth2/userinfo'

LOGIN_URL = '/admin/login/'

LOGIN_REDIRECT_URL = '/admin/'

LOGOUT_REDIRECT_URL = '/'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# File Storage

# Upload media files to bucket
DEFAULT_FILE_STORAGE = 'farafmb.storage.MediaStorage'

# Upload static files via collectstatic to bucket
STATICFILES_STORAGE = 'farafmb.storage.StaticStorage'

AWS_S3_ENDPOINT_URL = os.getenv('STORAGE_ENDPOINT_URL')

AWS_S3_ACCESS_KEY_ID = os.getenv('STORAGE_ACCESS_KEY')

AWS_S3_SECRET_ACCESS_KEY = os.getenv('STORAGE_SECRET_KEY')

STORAGE_MEDIA_FILES = os.getenv('STORAGE_MEDIA_BUCKET')

STORAGE_STATIC_FILES = os.getenv('STORAGE_STATIC_BUCKET')

# Default ACL on file. Otherwise, inheriting bucket ACL
AWS_DEFAULT_ACL = 'public-read'

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]


# E-Mail

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('EMAIL_HOST')

EMAIL_PORT = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER = os.getenv('EMAIL_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL')

SERVER_EMAIL = os.getenv('SERVER_EMAIL')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
