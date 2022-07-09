from django.db import models
from django.utils.translation import gettext_lazy as _


class Program(models.Model):
    class Faculties(models.TextChoices):
        FMB = 'MB', _("Mechanical Engineering")
        FVST = 'VST', _("Process and Systems Engineering")
        FEIT = 'EIT', _("Electrical Engineering and Information Technology")
        FMA = 'MA', _("Mathematics")
    faculty = models.CharField(max_length=3, choices=Faculties.choices, default=Faculties.FMB)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Study program")
        verbose_name_plural = _("Study programs")
        ordering = ['name']

    def __str__(self):
        return self.name


class Mentor(models.Model):
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(_("Mobile number"), max_length=25)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Mentor")
        verbose_name_plural = _("Mentors")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
