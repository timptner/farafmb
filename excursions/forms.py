from django import forms
from django.core.exceptions import ValidationError

from .models import Participant, Excursion


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
