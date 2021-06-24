from datetime import time
from django.core.exceptions import ValidationError
from django.db import models


def validate_time(value: time):
    if not (time(hour=7) <= value <= time(hour=19)):
        raise ValidationError("Es sind nur Zeiten zwischen 7 und 19 Uhr erlaubt.")


class OfficeHour(models.Model):
    is_visible = models.BooleanField(default=True)
    member = models.CharField(max_length=50)
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    DAYS = [
        (MONDAY, 'Montag'),
        (TUESDAY, 'Dienstag'),
        (WEDNESDAY, 'Mittwoch'),
        (THURSDAY, 'Donnerstag'),
        (FRIDAY, 'Freitag'),
    ]
    day = models.IntegerField(choices=DAYS)
    time = models.TimeField(validators=[validate_time])

    def __str__(self):
        return self.member
