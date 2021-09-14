from django.shortcuts import get_object_or_404
from django.views import generic

from .forms import ParticipantForm
from .models import Excursion, Participant


class ExcursionListView(generic.ListView):
    model = Excursion


class ExcursionDetailView(generic.DetailView):
    model = Excursion

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['registrations'] = Participant.objects.filter(excursion=kwargs['object']).count()
        return data


class ParticipantCreateView(generic.CreateView):
    model = Participant
    form_class = ParticipantForm
    success_url = 'success/'

    def form_valid(self, form):
        excursion = Excursion.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            participant = form.save(commit=False)
            participant.excursion = excursion
            participant.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['excursion'] = get_object_or_404(Excursion, pk=self.kwargs['pk'])
        return data
