import re

from django import forms
from django.core.mail import send_mass_mail
from django.core.exceptions import ValidationError
from django.forms.renderers import TemplatesSetting
from django.utils.translation import gettext_lazy as _

from .models import Participant, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'desc', 'registration_started_at', 'registration_stopped_at')
        help_texts = {
            'desc': _('You can use <a href="https://www.markdownguide.org">Markdown</a> to format your text.'),
        }


class ParticipantForm(forms.ModelForm):
    default_renderer = TemplatesSetting
    privacy = forms.BooleanField(label=_("Privacy"),
                                 widget=forms.CheckboxInput(attrs={
                                     'data-label': _("I accept the privacy statement and agree to "
                                                     "the processing of my personal data."),
                                 }))

    class Meta:
        model = Participant
        fields = ('event', 'first_name', 'last_name', 'email', 'comment')
        help_texts = {
            'email': _("Only email addresses with the domain 'st.ovgu.de' are allowed."),
        }
        widgets = {
            'event': forms.HiddenInput(),
        }

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        if not re.match(r'^([^@]*)@((st\.)?ovgu\.de)$', data):
            raise forms.ValidationError(_("Please use your university email address. "
                                          "(Did you even read the help text above? 🧐)"),
                                        code='forbidden_email')
        return data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     event: Event = cleaned_data.get('event')
    #     email = cleaned_data.get('email')
    #
    #     if event and email:
    #         if email in event.participant_set.values_list('email', flat=True):
    #             raise ValidationError(_("You are already registered for this event."))

    def save(self, commit=True):
        form = super()
        obj: Event = form.save(commit=False)
        if commit:
            obj.save()
        return obj


class ParticipantsContactForm(forms.Form):
    ALL = 'all'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    GROUP_CHOICES = [
        (ALL, _("All participants")),
        (APPROVED, _("Approved participants")),
        (REJECTED, _("Rejected participants")),
    ]
    group = forms.ChoiceField(label=_("Recipients"), choices=GROUP_CHOICES)
    subject = forms.CharField(label=_("Subject"), max_length=150, widget=forms.TextInput(attrs={'class': 'input'}))
    message = forms.CharField(label=_("Message"), widget=forms.Textarea(attrs={'class': 'textarea'}),
                              help_text=_("Use <code>{{ first_name }}</code> as a placeholder "
                                          "for the participants first name."))

    def send_email(self, event_pk):
        group = self.cleaned_data['group']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        participants = Participant.objects.filter(event__pk=event_pk)
        if group == self.APPROVED:
            participants = participants.filter(is_approved=True)
        elif group == self.REJECTED:
            participants = participants.filter(is_approved=False)
        else:
            pass

        mail_list = []
        for participant in participants:
            result = re.sub(r'{{\s*first_name\s*}}', participant.first_name, message, flags=re.IGNORECASE)
            mail = (subject, result, None, [participant.email])
            mail_list.append(mail)

        send_mass_mail(mail_list)
