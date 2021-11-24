import dj_database_url
import os
import sys

from django.core.management.utils import get_random_secret_key
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

DEBUG = os.getenv('DEBUG', "False") == "True"

ALLOWED_HOSTS = [
    "farafmb.de",
    "www.farafmb.de",
] + os.getenv('ALLOWED_HOSTS', "127.0.0.1,localhost").split(',')

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
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}


# Authentication

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

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'docker' / 'farafmb' / 'media'

STATIC_ROOT = BASE_DIR / 'docker' / 'farafmb' / 'static'


# E-Mail

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')

EMAIL_PORT = os.getenv('EMAIL_PORT', '25')

EMAIL_HOST_USER = os.getenv('EMAIL_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL', 'farafmb@ovgu.de')

SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'farafmb@ovgu.de')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
