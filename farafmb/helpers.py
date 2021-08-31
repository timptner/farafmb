import secrets

from django.utils import timezone


def get_random_filename_and_upload_to(path: str):
    if path.startswith('/') or path.endswith('/'):
        raise Exception("Path can't start or end with a slash ('/')")

    def get_random_filename(instance, filename: str) -> str:
        extension = filename.split('.')[-1].lower()
        token = secrets.token_urlsafe(10)
        iso_datetime = timezone.now().strftime("%Y%m%d")
        return f"{path}/{iso_datetime}_{token}.{extension}"

    return get_random_filename
