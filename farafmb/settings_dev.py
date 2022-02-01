from .settings import *

DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_ROOT = BASE_DIR / 'static'
