from markdown import markdown

from django.db import models


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
