from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic

from .forms import ParticipantForm
from .models import Excursion, Participant


class ExcursionListView(generic.ListView):
    model = Excursion
    ordering = '-date'


class ExcursionDetailView(generic.DetailView):
    model = Excursion

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['registrations'] = Participant.objects.filter(excursion=kwargs['object']).count()
        return data


class RegistrationFormView(generic.CreateView):
    template_name = 'excursions/registration_form.html'
    model = Participant
    form_class = ParticipantForm
    success_url = 'success/'

    def get_context_data(self, **kwargs):
        excursion = get_object_or_404(Excursion, pk=self.kwargs['pk'])
        data = super().get_context_data(**kwargs)
        data['excursion'] = excursion
        if excursion.registration_begins_at:
            data['show_pre_notification'] = timezone.now() < excursion.registration_begins_at
        else:
            data['show_pre_notification'] = False
        data['show_post_notification'] = timezone.now() > excursion.registration_ends_at
        data['show_archived_notification'] = timezone.now().date() > excursion.date  # TODO Fix 2h offset
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['excursion'] = get_object_or_404(Excursion, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        excursion = Excursion.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            participant = form.save(commit=False)
            participant.excursion = excursion
            participant.save()
            send_mail(
                f"Bestätigung deiner Anmeldung",
                "Hallo %s,\n\ndu hast dich erfolgreich für die Exkursion %s am %s angemeldet. Aktuell stehst du als %s "
                "auf der Liste. %s\n\nViele Grüße\nFachschaftsrat Maschinenbau" % (
                    participant.first_name,
                    excursion.title,
                    excursion.date.strftime('%d.%m.%Y'),
                    "Teilnehmer:in" if participant.is_seat_owner() else "Nachrücker:in",
                    "Wir werden dich kurz vor der Exkursion noch einmal kontaktieren um die letzten Details "
                    "abzusprechen." if participant.is_seat_owner() else
                    "Sollte ein:e Teilnehmer:in absagen, werden wir dich über den freien Platz informieren.",
                ),
                None,
                [participant.email],
            )
        return super().form_valid(form)


class RegistrationFormDoneView(generic.TemplateView):
    template_name = 'excursions/registration_form_done.html'
