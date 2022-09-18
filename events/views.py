import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import ParticipantForm, ParticipantsContactForm
from .models import Event, Participant


class InfoView(generic.DetailView):
    template_name = 'events/info.html'
    model = Event


class RegistrationView(generic.CreateView):
    template_name = 'events/registration_form.html'
    form_class = ParticipantForm
    success_url = 'done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.request.resolver_match.kwargs['pk'])
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


class ParticipantView(LoginRequiredMixin, generic.ListView):
    template_name = 'events/participants.html'
    model = Participant

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return Participant.objects.filter(event=event).order_by('registered_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['pk'])
        return context


class EventsView(LoginRequiredMixin, generic.ListView):
    template_name = 'events/events.html'
    model = Event


class ParticipantsContactView(LoginRequiredMixin, generic.FormView):
    template_name = 'events/participants_contact.html'
    form_class = ParticipantsContactForm
    success_url = 'done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['participants'] = Participant.objects.filter(event__pk=self.kwargs['pk']).all()
        return context

    def form_valid(self, form):
        form.send_email(event_pk=self.kwargs['pk'])
        return super().form_valid(form)


class ParticipantsContactDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'events/participants_contact_done.html'


@login_required()
def export_participants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants = event.participant_set.all()

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="participants.csv"'}
    )

    writer = csv.writer(response)
    writer.writerow([
        _("First name"),
        _("Last name"),
        _("Email"),
        _("Mobile number"),
        _("Comment"),
        _("Moment of registration"),
        _("Approval of registration"),
    ])
    for participant in participants:
        writer.writerow([
            participant.first_name,
            participant.last_name,
            participant.email,
            participant.mobile,
            participant.comment,
            participant.registered_at,
            _("Yes") if participant.is_approved else _("No"),
        ])

    return response
