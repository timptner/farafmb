from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField('members')
    biography = models.CharField(max_length=250)
    jobs = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    birthday = models.DateTimeField(blank=True, null=True)
    joined_at = models.DateTimeField()
