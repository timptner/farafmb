import secrets

from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_random_filename(instance, filename: str) -> str:
    extension = filename.split('.')[-1].lower()
    token = secrets.token_urlsafe(10)
    iso_datetime = timezone.now().strftime("%Y%m%d")
    return f"members/{iso_datetime}_{token}.{extension}"


class Profile(models.Model):
    EMO = 'EMO'
    IDE = 'IDE'
    MB = 'MB'
    MTK = 'MTK'
    SEM = 'SEM'
    WLO = 'WLO'
    WMB = 'WMB'
    COURSES = [
        (EMO, 'Elektromobilität'),
        (IDE, 'Integrated Design Engineering'),
        (MB, 'Maschinenbau'),
        (MTK, 'Mechatronik'),
        (SEM, 'Systems Engineering for Manufacturing'),
        (WLO, 'Wirtschaftsingenieur Logistik'),
        (WMB, 'Wirtschaftsingenieur Maschinenbau'),
    ]
    BSC = 'BSC'
    MSC = 'MSC'
    DEGREES = [
        (BSC, 'Bachelor of Science'),
        (MSC, 'Master of Science'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_random_filename)
    biography = models.CharField(max_length=250, blank=True)
    jobs = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=3, choices=COURSES)
    degree = models.CharField(max_length=3, choices=DEGREES)
    birthday = models.DateField(blank=True, null=True)
    joined_at = models.DateField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_job_list(self):
        return [job.strip() for job in self.jobs.split(',')]

    def is_cakeday(self):
        today = date.today()
        return self.birthday.month == today.month and self.birthday.day == today.day
