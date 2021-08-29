from django.db import models
from django.contrib.auth.models import User


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
    picture = models.ImageField('members')
    biography = models.CharField(max_length=250, blank=True)
    jobs = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=3, choices=COURSES)
    birthday = models.DateField(blank=True, null=True)
    joined_at = models.DateField()

    def __str__(self):
        return self.user.get_full_name() or self.user.username
