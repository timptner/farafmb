import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ['SECRET_KEY']


# Application definition

INSTALLED_APPS = [
    'blog',
    'jobs',
    'meetings',

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
        },
    },
]

WSGI_APPLICATION = 'farafmb.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'farafmb',
        'USER': 'farafmb',
        'PASSWORD': os.getenv('SQL_PASSWORD', ''),
        'HOST': os.getenv('SQL_HOST', ''),
        'PORT': os.getenv('SQL_PORT', ''),
    }
}


# Authentication

AUTHENTICATION_BACKENDS = [
    'farafmb.auth.KeycloakBackend',
    'django.contrib.auth.backends.ModelBackend',
]

OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID', '')

OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET', '')

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

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# File Storage

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]

MEDIA_URL = '/media/'


# E-Mail

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('MAIL_HOST', 'localhost')

EMAIL_PORT = os.getenv('MAIL_PORT', '25')

EMAIL_HOST_USER = os.getenv('MAIL_USER', '')

EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASSWORD', '')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@faking.cool')

SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'noreply@faking.cool')
