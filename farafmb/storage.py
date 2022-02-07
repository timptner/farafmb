from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
from urllib.parse import urlparse


class StaticStorage(S3StaticStorage):
    bucket_name = settings.STORAGE_STATIC_BUCKET
    custom_domain = urlparse(settings.STATIC_URL).netloc


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.STORAGE_MEDIA_BUCKET
    custom_domain = urlparse(settings.MEDIA_URL).netloc
