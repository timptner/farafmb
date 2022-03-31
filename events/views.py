from django.http import HttpResponseForbidden
from django.utils import timezone
from django.views import generic

from .forms import ParticipantForm
from .models import Event


class InfoView(generic.DetailView):
    template_name = 'events/info.html'
    model = Event


class RegistrationView(generic.CreateView):
    template_name = 'events/registration_form.html'
    form_class = ParticipantForm
    success_url = 'done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update({'event': self.request.resolver_match.kwargs['pk']})
        return kwargs

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['pk'])
        if event.registration_status() == 'pending':
            return HttpResponseForbidden(f"Registration will open at {event.registration_started_at} UTC")
        if event.registration_status() == 'closed':
            return HttpResponseForbidden(f"Registration closed since {event.registration_stopped_at} UTC")
        return super().post(request, *args, **kwargs)


class RegistrationDoneView(generic.TemplateView):
    template_name = 'events/registration_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        return context
