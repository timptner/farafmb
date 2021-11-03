from django.contrib import admin
from django.db import models
from django.utils import timezone


class Job(models.Model):
    JOB = 'job'
    THESIS = 'thesis'
    INTERNSHIP = 'internship'
    SIDELINE = 'sideline'
    GROUP_CHOICES = [
        (JOB, "Job"),
        (THESIS, "Abschlussarbeit"),
        (INTERNSHIP, "Praktikum"),
        (SIDELINE, "Nebentätigkeit"),
    ]
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    desc = models.TextField('description')
    expired_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @admin.display(boolean=True)
    def is_expired(self):
        if not self.expired_on:
            return False
        return self.expired_on < timezone.now()


def job_directory_path(instance, filename):
    return f'jobs/{instance.job.slug}/{filename}'


class Document(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=job_directory_path)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
