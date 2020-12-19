import bleach
import secrets

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from markdown import markdown
from pathlib import Path


def generate_random_name(instance, filename: str) -> str:
    time = int(datetime.now().timestamp())
    name = secrets.token_hex(3)
    suffix = filename.split('.')[-1]
    return f"blog/{time}_{name}.{suffix.lower()}"


class Snippet(models.Model):
    slug = models.SlugField(unique=True)
    desc = models.CharField('description', max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc

    def clean(self):
        self.content = bleach.clean(self.content, tags=[], strip=True)

    def render(self):
        cleaned = bleach.clean(self.content, strip=True)
        return markdown(cleaned, extensions=['tables'])


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True)
    video = models.ForeignKey('Video', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        self.content = bleach.clean(self.content, tags=[], strip=True)

    def edited(self):
        return self.created + timedelta(minutes=5) < self.updated

    def render(self):
        cleaned = bleach.clean(self.content, strip=True)
        return markdown(cleaned)


class Image(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to=generate_random_name)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=generate_random_name)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=generate_random_name)
    created = models.DateTimeField(auto_now_add=True)

    def extension(self):
        path = Path(self.file.path)
        return path.suffix[1:]

    def icon(self):
        suffix = self.extension()

        if suffix == 'pdf':
            return "fas fa-file-pdf"

        if suffix == 'zip':
            return "fas fa-file-archive"

        return "fas fa-file"
