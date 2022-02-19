import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

SECRET_KEY = os.environ['SECRET_KEY']


# Application definition

INSTALLED_APPS = [
    'about',
    'accounts',
    'blog',
    'consultations',
    'documents',
    'exams',
    'excursions',
    'jobs',
    'meetings',
    'members',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'oauth2_provider',
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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication

LOGIN_REDIRECT_URL = '/admin/'

LOGOUT_REDIRECT_URL = '/'

OAUTH2_PROVIDER = {
    'OIDC_ENABLED': True,
    'OIDC_RSA_PRIVATE_KEY': os.getenv('OIDC_RSA_PRIVATE_KEY'),
    'SCOPES': {
        'openid': 'OpenID Connect scope',
        'profile': 'User profile scope',
        'email': 'User email scope',
    },
    'OAUTH2_VALIDATOR_CLASS': 'farafmb.oauth.CustomOAuth2Validator',
}


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

USE_TZ = True


# File Storage

STATICFILES_DIRS = [
    BASE_DIR / 'farafmb' / 'static',
]

STATIC_URL = '/static/'

STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'files' / 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.getenv('MEDIA_ROOT', BASE_DIR / 'files' / 'media')


# Email

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('EMAIL_HOST')

EMAIL_PORT = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER = os.getenv('EMAIL_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')


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
            'filename': os.getenv('LOG_FILE', './server.log'),
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
