from decouple import config
from dj_database_url import parse as db_url
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'about',
    'accounts',
    'blog',
    'consultations',
    'documents',
    'events',
    'exams',
    'jobs',
    'links',
    'meetings',
    'members',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
            'libraries': {
                'markdown': 'farafmb.templatetags.markdown',
            },
        },
    },
]

WSGI_APPLICATION = 'farafmb.wsgi.application'


# Database

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        cast=db_url,
    )
}


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication

LOGIN_REDIRECT_URL = reverse_lazy('members:member-list')


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

LANGUAGE_CODE = 'de'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'farafmb' / 'locale',
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# File Storage

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]

DEFAULT_FILE_STORAGE = config('MEDIA_FILE_STORAGE', default='django.core.files.storage.FileSystemStorage')

STATICFILES_STORAGE = config('STATIC_FILE_STORAGE', default='django.contrib.staticfiles.storage.StaticFilesStorage')

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

AWS_S3_ENDPOINT_URL = config('BUCKET_ENDPOINT_URL', default='')

AWS_STORAGE_BUCKET_NAME = config('BUCKET_NAME', default='')

AWS_ACCESS_KEY_ID = config('BUCKET_ACCESS_KEY', default='')

AWS_SECRET_ACCESS_KEY = config('BUCKET_SECRET_KEY', default='')

AWS_S3_CUSTOM_DOMAIN = config('BUCKET_DOMAIN', default='')


# Email

EMAIL_HOST = config('EMAIL_HOST', default='localhost')

EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)

EMAIL_HOST_USER = config('EMAIL_USER', default='')

EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default='')

EMAIL_USE_TLS = config('EMAIL_SECURE', default=False, cast=bool)

DEFAULT_FROM_EMAIL = config('DEFAULT_EMAIL', 'hello@farafmb.de')

SERVER_EMAIL = config('SERVER_EMAIL', 'hello@farafmb.de')


# Forms

FORM_RENDERER = 'farafmb.forms.BulmaFormRenderer'


# Security

# SECURE_SSL_REDIRECT = True
#
# SECURE_HSTS_SECONDS = 365*24*60*60
#
# SECURE_HSTS_PRELOAD = True
#
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#
# SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
#
# SESSION_COOKIE_SECURE = True
#
# CSRF_COOKIE_SECURE = True


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[{asctime}] {levelname} {message}',
            'style': '{',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': config('LOG_FILE', default='./server.log'),
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
