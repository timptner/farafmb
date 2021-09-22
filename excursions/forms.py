from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Participant, Excursion


class ExcursionForm(forms.ModelForm):
    desc = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "vLargeTextField",
            'style': "font-family: 'Source Code Pro', 'Courier New', monospace;",
        }),
        help_text="You can format this text with Markdown",
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['registration_begins_at'] < cleaned_data['registration_ends_at']:
            raise forms.ValidationError({'registration_begins_at': "Registration can't begin after it has ended."})


def convert_email(value: str) -> str:
    """Convert email domain from student to employee or vice versa"""
    user, domain = value.split('@')
    if domain.startswith('st.'):
        return f"{user}@{domain[3:]}"
    else:
        return f"{user}@st.{domain}"


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('first_name', 'last_name', 'email', 'phone', 'is_car_owner')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
        }
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail-Adresse",
            'phone': "Mobilnummer",
            'is_car_owner': "Fahrbereitschaft",
        }

    def __init__(self, *args, **kwargs):
        self.excursion: Excursion = kwargs.pop('excursion', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        data = self.cleaned_data['email']
        email_list = self.excursion.participant_set.values_list('email', flat=True)
        if data in email_list:
            raise ValidationError("Ein:e Student:in mit dieser E-Mail-Adresse ist bereits "
                                  "für die Exkursion angemeldet.",
                                  code='already registered')
        if convert_email(data) in email_list:
            raise ValidationError("Ein:e Student:in ist bereits mit der alternativen E-Mail-Adresse "
                                  "'%(email)s' für die Exkursion angemeldet.",
                                  params={'email': convert_email(data)},
                                  code='corresponding email already used')
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        data.replace(' ', '')
        return data

    def clean(self):
        cleaned_data = super().clean()
        if timezone.now() >= self.excursion.registration_ends_at:
            raise ValidationError("Die Anmeldung ist leider nicht mehr möglich.", code='registration closed')

        if self.excursion.registration_begins_at:
            if timezone.now() < self.excursion.registration_begins_at:
                raise ValidationError("Die Anmeldung ist noch nicht möglich. Versuche es später noch einmal.",
                                      code='registration not started')
