from django.db import models
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    url = models.URLField(_("URL"))
    text = models.CharField(_("Text"), max_length=100)
    icon = models.CharField(_("Icon"), max_length=50, blank=True)
    position = models.PositiveSmallIntegerField(_("Position"), unique=True)
    is_active = models.BooleanField(_("Active"), default=False)

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
        ordering = ['position']

    def __str__(self):
        return self.text
