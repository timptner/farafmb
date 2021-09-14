from django import forms

from .models import Participant


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
