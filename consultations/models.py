from datetime import time
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_time(value: time):
    if not (time(hour=7) <= value <= time(hour=19)):
        raise ValidationError(_("Only times between 7 a.m. and 7 p.m. are allowed."))


class Consultation(models.Model):
    is_visible = models.BooleanField(_("Visibility"), default=True)
    member = models.CharField(_("Member"), max_length=50)
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    DAYS = [
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
    ]
    day = models.IntegerField(_("Day"), choices=DAYS)
    time = models.TimeField(_("Time"), validators=[validate_time])

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")

    def __str__(self):
        return self.member
