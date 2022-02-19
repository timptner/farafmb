from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Exam(models.Model):
    course = models.CharField(_("Course"), max_length=150)
    lecturer = models.CharField(_("Lecturer"), max_length=100)
    date = models.DateField(_("Date of the exam"))
    minute_author = models.EmailField(_("Author of the minute"), null=True)
    minute_file = models.FileField(_("Minute file"), upload_to='exams/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf']),
    ])
    submitted_on = models.DateTimeField(_("Submitted on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")

    def __str__(self):
        return self.course
