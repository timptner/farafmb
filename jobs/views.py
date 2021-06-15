from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from .models import Job


class JobList(generic.ListView):
    model = Job
    queryset = Job.objects.exclude(expired_on__lt=timezone.now())
    ordering = '-created_on'
