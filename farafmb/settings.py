import os
from pathlib import Path

from django.core.management import utils
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / ".data"

SECRET_KEY = os.getenv("SECRET_KEY", utils.get_random_secret_key())

DEBUG = os.getenv("DEBUG", "no").lower() in ["yes", "true"]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INTERNAL_IPS = ["127.0.0.1"]

SITE_ID = 1


# Application definition

INSTALLED_APPS = [
    "accounts",
    "blog",
    "consultations",
    "documents",
    "excursions",
    "exams",
    "home",
    "jobs",
    "links",
    "meetings",
    "members",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "farafmb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "farafmb" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "markdown": "farafmb.templatetags.markdown",
            },
        },
    },
]

WSGI_APPLICATION = "farafmb.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DATABASE_HOST", ""),
        "PORT": os.getenv("DATABASE_PORT", ""),
        "NAME": os.getenv("DATABASE_NAME", "farafmb"),
        "USER": os.getenv("DATABASE_USER", "farafmb"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
    }
}


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication

LOGIN_REDIRECT_URL = reverse_lazy("members:member-list")


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "de"

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "farafmb" / "locale",
]

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# File Storage

STATICFILES_DIRS = [
    BASE_DIR / "farafmb" / "static",
]

STATIC_URL = "static/"

STATIC_ROOT = os.getenv("STATIC_ROOT", DATA_DIR / "static")

MEDIA_URL = "media/"

MEDIA_ROOT = os.getenv("MEDIA_ROOT", DATA_DIR / "media")


# Email

EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")

EMAIL_PORT = os.getenv("EMAIL_PORT", 25)

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "yes") in ["yes", "true"]

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "hello@farafmb.de")

SERVER_EMAIL = os.getenv("SERVER_EMAIL", "server@farafmb.de")


# Forms

FORM_RENDERER = "farafmb.forms.BulmaFormRenderer"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_FILE", str(DATA_DIR / "logs" / "server.log")),
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
