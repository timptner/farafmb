from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic

from .forms import ParticipantForm, ContactForm
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

    def get_success_url(self):
        return reverse_lazy('excursions:registration_done', kwargs={'pk': self.kwargs['pk']})

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
        data['car_checkbox_text'] = "Ich besitze ein Auto und wäre bereit eine Fahrgemeinschaft zu bilden."
        data['privacy'] = (
            "Wir benötigen deinen vollständigen Namen sowie deine E-Mail-Adresse zur Bestätigung deiner Teilnahme an "
            "der Exkursion gegenüber der Fakultät. Deine eben genannten Daten werden an das Prüfungsamt, sowie in "
            "einigen Fällen an das zu besichtigende Unternehmen, weitergegeben. Deine Mobilnummer verwenden wir, um "
            "dich kurzfristig am Tag der Exkursion erreichen zu können. Deine Mobilnummer wird von uns nicht an "
            "Dritte weitergegeben. Alle deine Daten werden von uns vertraulich behandelt und nach Ablauf einer Frist "
            "von 6 Monaten unwiderruflich gelöscht."
        )
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


class ContactFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    permission_required = ('excursions.add_excursion', 'excursions.edit_excursion', 'excursions.delete_excursion')
    template_name = 'excursions/contact_form.html'
    form_class = ContactForm
    success_url = '/admin/excursions/participant/'  # TODO use reverse_lazy to get admin page

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            pk_list = [int(pk) for pk in self.request.GET.get('ids', '').split(',')]
            data['participants'] = Participant.objects.filter(pk__in=pk_list).order_by('first_name', 'last_name').all()
        except ValueError:
            pass
        return data

    def form_valid(self, form):
        if form.is_valid():
            try:
                pk_list = [int(pk) for pk in self.request.GET.get('ids', '').split(',')]
                recipients = Participant.objects.filter(pk__in=pk_list).values_list('email', flat=True)
                form.send_emails(recipients)
                messages.success(self.request, "%s emails were sent successfully." % len(recipients))
            except ValueError:
                messages.error(self.request, "No emails were sent because the recipient list is empty.")
        return super().form_valid(form)
