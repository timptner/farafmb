import django_heroku
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['farafmb.de']


# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'meetings.apps.MeetingsConfig',
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
        'DIRS': [
            BASE_DIR / 'farafmb' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'farafmb.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_HOST_USER'),
        'PASSWORD': os.getenv('DB_HOST_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Authentication

AUTHENTICATION_BACKENDS = [
    'farafmb.auth.KeycloakBackend',
    'django.contrib.auth.backends.ModelBackend',
]

OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID')

OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET')

OIDC_RP_SIGN_ALGO = "RS256"

OIDC_OP_JWKS_ENDPOINT = "https://auth.faking.cool/auth/realms/faking/protocol/openid-connect/certs"

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://auth.faking.cool/auth/realms/faking/protocol/openid-connect/auth"

OIDC_OP_TOKEN_ENDPOINT = "https://auth.faking.cool/auth/realms/faking/protocol/openid-connect/token"

OIDC_OP_USER_ENDPOINT = "https://auth.faking.cool/auth/realms/faking/protocol/openid-connect/userinfo"

LOGIN_REDIRECT_URL = "/admin/"

LOGOUT_REDIRECT_URL = "/"


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

LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]

STATIC_ROOT = BASE_DIR / 'static'


# Media files (Images, Documents)

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# E-Mail

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('EMAIL_HOST')

EMAIL_PORT = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'farafmb@ovgu.de'


# Security

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# Activate Django-Heroku.

django_heroku.settings(locals())
