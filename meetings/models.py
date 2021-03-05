from django.conf import settings
from django.db import models


class Meeting(models.Model):
    date = models.DateField(unique=True)
    recorder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    agenda = models.TextField()
    guests = models.TextField(blank=True)

    def __str__(self):
        return str(self.date)


class Template(models.Model):
    slug = models.SlugField(unique=True)
    content = models.TextField()

    def __str__(self):
        return self.slug

# class Minute(models.Model):
#     meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True)
#     content = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.meeting.date
