import os

from django.conf import settings
from django.shortcuts import render
from django_s3_storage.storage import S3Storage

storage = S3Storage(
    aws_region=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_s3_bucket_name=os.getenv('DO_SPACE_NAME_DOCS', 'farafmb-docs'),
    aws_s3_endpoint_url=os.getenv('DO_SPACE_ENDPOINT_URL_DOCS', 'https://fra1.digitaloceanspaces.com'),
    aws_s3_file_overwrite=True,
)


def list_pages(request):
    response = storage.s3_connection.list_objects_v2(Bucket=storage.settings.AWS_S3_BUCKET_NAME)
    files = []
    for entry in response.get('Contents', []):
        key = entry['Key'].rstrip('.md')
        files.append({'key': key, 'name': key.replace('_', ' ')})
    return render(request, 'docs/list_pages.html', {'files': files})

