from django.db import models
from django.utils.translation import gettext_lazy as _


class Consultation(models.Model):
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
    start = models.TimeField(_("Start"))
    end = models.TimeField(_("End"))
    text = models.CharField(_("Text"), max_length=50)

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")
        ordering = ['day', 'start']

    def __str__(self):
        return self.text
