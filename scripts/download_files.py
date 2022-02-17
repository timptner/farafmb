#!/usr/bin/env python3

import boto3
import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

destination = '/var/www/farafmb.de/media'

storage = boto3.resource(
    service_name='s3',
    endpoint_url=os.getenv('STORAGE_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('STORAGE_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('STORAGE_SECRET_KEY'),
)

bucket = storage.Bucket('farafmb-media')


def get_all_files(path: str):
    folders, files = bucket.listdir(path + '/')
    if files:
        yield ['/'.join([path, file]) for file in files]
    for folder in folders:
        yield from get_all_files('/'.join([path, folder]))


def main():
    """Main entry-point for script."""
    files = []
    for items in get_all_files(''):
        files.extend(items)
    print(f'Found {len(files)} files in bucket')

    for file in files:
        local = os.path.join(destination, file)
        bucket.download_file(file, local)
        print(f'New file created: {local}')


if __name__ == '__main__':
    main()
