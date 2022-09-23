from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    email = models.EmailField(_("Email address"))
    items = models.JSONField(_("Items"))
    is_verified = models.BooleanField(_("Is verified"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['created_at']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Token(models.Model):
    key = models.SlugField(max_length=50, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
