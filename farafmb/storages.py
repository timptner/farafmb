from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    location = 'static'
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
