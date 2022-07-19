from django.db import models
from django.utils.translation import gettext_lazy as _


class Registration(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    started_at = models.DateTimeField(_("Started at"))
    stopped_at = models.DateTimeField(_("Stopped at"))
    is_helper_form_active = models.BooleanField(_("Is helper form active?"), default=False)
    helper_form_desc = models.TextField(_("Description text for helper form"), blank=True)

    class Meta:
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("Study program")
        verbose_name_plural = _("Study programs")

    def __str__(self):
        return self.name


class Mentor(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name=_("Registration"))
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(_("Mobile number"), max_length=25)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, verbose_name=_("Study program"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Mentor")
        verbose_name_plural = _("Mentors")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Helper(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name=_("Registration"))
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(_("Mobile number"), max_length=25)
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Helper")
        verbose_name_plural = _("Helpers")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
