#!/usr/bin/env python3

import sys

from django.core.files.storage import default_storage
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.extend([str(BASE_DIR)])

load_dotenv()


def get_all_files(path: str):
    folders, files = default_storage.listdir(path + '/')
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
        default_storage.delete(file)
    print('Deleted all files')


if __name__ == '__main__':
    main()
