from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from .models import Job


class JobList(generic.ListView):
    model = Job
    ordering = '-created_on'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['groups'] = Job.GROUP_CHOICES
        return data

    def get_queryset(self):
        queryset = Job.objects.exclude(expired_on__lt=timezone.now())
        if 'group' in self.request.GET:
            queryset = queryset.filter(group=self.request.GET['group'])
        return queryset
