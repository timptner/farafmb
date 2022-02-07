from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    bucket_name = settings.STORAGE_STATIC_BUCKET
    custom_domain = settings.STORAGE_STATIC_DOMAIN


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.STORAGE_MEDIA_BUCKET
    custom_domain = settings.STORAGE_MEDIA_DOMAIN
