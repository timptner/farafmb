from datetime import date
from django.db import models
from django.contrib.auth.models import User

from farafmb.helpers import get_random_filename_and_upload_to


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_random_filename_and_upload_to('members'))
    biography = models.CharField(max_length=250, blank=True)
    jobs = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=3, choices=COURSES)
    birthday = models.DateField(blank=True, null=True)
    joined_at = models.DateField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_job_list(self):
        return [job.strip() for job in self.jobs.split(',')]

    def is_cakeday(self):
        today = date.today()
        return self.birthday.month == today.month and self.birthday.day == today.day
