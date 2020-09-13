from datetime import datetime
from markdown import markdown

from django.db import models
from django.contrib.auth.models import User


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
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def edited(self):  # TODO
        # created = self.created.replace(microseconds=0)
        # updated = self.updated.replace(microseconds=0)
        return False

    def html(self):
        return markdown(self.content, extensions=['tables'])
