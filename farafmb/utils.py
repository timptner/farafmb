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
