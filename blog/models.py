from datetime import datetime
from markdown import markdown
from secrets import token_hex

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def generate_random_name(instance, filename):
    path = settings.MEDIA_ROOT
    files = [file.stem for file in path.iterdir()]
    file = token_hex(3)
    while file in files:
        file = token_hex(3)

    suffix = filename.split('.')[-1]
    return f"blog/{file}.{suffix}"


class Snippet(models.Model):
    key = models.SlugField(unique=True)
    desc = models.CharField('description', max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc

    def html(self):
        return markdown(self.content, extensions=['tables'])


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def edited(self):  # TODO access fields as python datetime objects
        # created = self.created.replace(microseconds=0)
        # updated = self.updated.replace(microseconds=0)
        return False

    def html(self):
        return markdown(self.content, extensions=['tables'])


class Image(models.Model):
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to=generate_random_name)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
