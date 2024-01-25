from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    title = models.CharField(max_length=100)
    file = models.ImageField(upload_to='about/')

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self) -> str:
        return self.title
