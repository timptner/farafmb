from django.contrib import admin
from django.core.files import File
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from secrets import token_urlsafe


def validate_file_extension(value: File):
    """Check if uploaded file content is pdf"""
    if value.file.content_type != 'application/pdf':
        raise ValidationError("Only PDF are allowed")


def user_directory_path(instance: File, filename: str) -> str:
    """Return a unix-like storage path as string with random file name"""
    filename = token_urlsafe(5) + '.pdf'
    filepath = f"jobs/{filename}"
    if Job.objects.filter(file=filepath).exists():
        return user_directory_path(instance, filename)
    return filepath


class Job(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], blank=True, null=True)
    expired_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean_fields(self, exclude=None):
        try:
            super().clean_fields(exclude=exclude)
        except AttributeError:
            # Handle missing content_type on file object
            pass

    @admin.display(boolean=True)
    def is_expired(self):
        if not self.expired_on:
            return False
        return self.expired_on < timezone.now()
