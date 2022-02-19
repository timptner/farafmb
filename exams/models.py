from django.core.validators import FileExtensionValidator
from django.db import models


class Exam(models.Model):
    course = models.CharField(max_length=150)
    lecturer = models.CharField(max_length=100)
    date = models.DateField()
    minute_author = models.EmailField(null=True)
    minute_file = models.FileField(upload_to='exams/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course
