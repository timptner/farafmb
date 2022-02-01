#!/usr/bin/env python3

import boto3
import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

source = '/home/aiven/Downloads/media'

storage = boto3.resource(
    service_name='s3',
    endpoint_url=os.getenv('STORAGE_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('STORAGE_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('STORAGE_SECRET_KEY'),
)


def main():
    """Main entry-point for script."""
    bucket = storage.Bucket('farafmb')

    for prefix, folders, files in os.walk(source):
        if not files:
            continue
        for file in files:
            local = os.path.join(prefix, file)
            remote = os.path.relpath(local, source)
            bucket.upload_file(local, remote, ExtraArgs={'ACL': 'public-read'})
            print(f'New file created: {remote}')


if __name__ == '__main__':
    main()
