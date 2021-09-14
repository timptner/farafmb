from django.shortcuts import render
from django.views import generic

from .models import Excursion, Participant


class ExcursionListView(generic.ListView):
    model = Excursion


class ExcursionDetailView(generic.DetailView):
    model = Excursion

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['registrations'] = Participant.objects.filter(excursion=kwargs['object']).count()
        return data
