import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

PROJECT_DIR = Path(__file__).resolve(strict=True).parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = (os.getenv('TARGET_ENV') == 'development')

ALLOWED_HOSTS = ['dev.farafmb.de', 'farafmb.de', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
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
            PROJECT_DIR / 'templates',
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
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
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
    PROJECT_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'static'


# Media files (Images, Documents)

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# E-Mail

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('SMTP_HOST')

EMAIL_PORT = os.getenv('SMTP_PORT')

EMAIL_HOST_USER = os.getenv('SMTP_USERNAME')

EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD')

DEFAULT_FROM_EMAIL = 'farafmb@ovgu.de'


# Security

SECURE_HSTS_SECONDS = 3600  # TODO set value to 31536000 (1 year)

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
