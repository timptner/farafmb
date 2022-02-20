import os
import random
import string


def generate_random_file_name(length: int = 8, suffix: str = None) -> str:
    """Generate a random file name of specific length"""
    chars = string.ascii_letters + string.digits
    random.seed = (os.urandom(1024))
    file_name = ''.join(random.choice(chars) for i in range(length))
    if suffix:
        file_name = file_name + suffix
    return file_name


def human_bytes(byte: int, precision: int = 2) -> str:
    """Return a human readable version of the byte amount"""
    kilo_byte = 10 ** 3
    mega_byte = 10 ** 6
    giga_byte = 10 ** 9
    tera_byte = 10 ** 12
    if byte >= tera_byte:
        return f"{round(byte / tera_byte, precision)} TB"
    elif byte >= giga_byte:
        return f"{round(byte / giga_byte, precision)} GB"
    elif byte >= mega_byte:
        return f"{round(byte / mega_byte, precision)} MB"
    elif byte >= kilo_byte:
        return f"{round(byte / kilo_byte, precision)} kB"
    return f"{byte} B"
