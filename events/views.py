from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import ParticipantForm
from .models import Event, Participant


class InfoView(generic.DetailView):
    template_name = 'events/info.html'
    model = Event


class RegistrationView(generic.CreateView):
    template_name = 'events/registration_form.html'
    form_class = ParticipantForm
    success_url = 'done/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update({'event': self.request.resolver_match.kwargs['pk']})
        return kwargs


class RegistrationDoneView(generic.TemplateView):
    template_name = 'events/registration_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return context
