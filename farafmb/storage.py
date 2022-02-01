from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.STORAGE_MEDIA_FILES


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.STORAGE_STATIC_FILES
    querystring_auth = False  # Keep url consistent
