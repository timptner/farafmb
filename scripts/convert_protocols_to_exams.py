#!/usr/bin/env python3

import json

from pathlib import Path


def get_valid_file_path(file_path: str) -> Path:
    """Check if file exists and return valid Path object"""
    path = Path(file_path).resolve()
    if not path.is_file():
        raise Exception("No file found! Please check your path and try again.")

    return path


def convert_data(data: list) -> list:
    """Convert fixture to new format"""
    print(f"Found {len(data)} entries, updating ... ", end='')
    for item in data:
        item['model'] = 'exams.exam'
        fields: dict = item['fields']
        fields['minute_author'] = fields.pop('author')
        fields['minute_file'] = fields.pop('file')
        fields['submitted_on'] = fields.pop('submitted')
        fields['is_archived'] = False
    print('Done!')
    return data


def get_valid_folder_path(folder_path: str) -> Path:
    """Check if folder exists and return valid Path object"""
    path = Path(folder_path).resolve()
    if not path.parent.is_dir():
        raise Exception("No folder found! Please check your path and try again.")

    return path


def main():
    """Main entry-point for script"""
    source = input("Please specify a file path where the dump file can be found.\n> ")
    path = get_valid_file_path(source)
    data: list = json.loads(path.read_text())
    data = convert_data(data)
    destination = input("Please specify a folder path where the new dump file should be stored.\n> ")
    path = get_valid_folder_path(destination)
    file = path / 'exams.json'
    if file.exists():
        raise Exception("File 'exams.json' already exists! Please move or delete the existing file first.")
    else:
        (path / 'exams.json').write_text(json.dumps(data, ensure_ascii=False))
        print("New file 'exams.json' created!")


if __name__ == '__main__':
    main()
