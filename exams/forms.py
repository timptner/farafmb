from django import forms
from django.utils import timezone

from .models import Protocol


class ProtocolForm(forms.ModelForm):
    privacy = forms.BooleanField(label="Datenschutz")

    class Meta:
        model = Protocol
        fields = ['author', 'course', 'lecturer', 'date', 'file']
        labels = {
            'author': "E-Mail-Adresse",
            'course': "Modul",
            'lecturer': "Dozent:in",
            'date': "Datum der Prüfung",
            'file': "Datei",
        }
        widgets = {
            'author': forms.EmailInput(attrs={'class': "input"}),
            'course': forms.TextInput(attrs={'class': "input"}),
            'lecturer': forms.TextInput(attrs={'class': "input"}),
            'date': forms.DateInput(attrs={'type': "date", 'class': "input"}),
            'file': forms.FileInput(attrs={'class': "file-input"})
        }
        help_texts = {
            'author': "Es sind nur E-Mail-Adressen mit der Domain 'st.ovgu.de' erlaubt.",
            'file': "Es können nur PDF-Dateien mit einer Größe von maximal 2 MB eingereicht werden.",
        }

    def clean_author(self):
        data = self.cleaned_data['author']
        if data.split('@')[-1] != 'st.ovgu.de':
            raise forms.ValidationError("Es kann nur die erlaubte Domain verwendet werden!", code='invalid')
        return data

    def clean_date(self):
        data = self.cleaned_data['date']
        if data > timezone.now().date():
            raise forms.ValidationError("Das Datum darf nicht in der Zukunft liegen.", code='invalid_date')
        return data

    def clean_file(self):
        data = self.cleaned_data['file']
        if data.size > 2 * 10**6:
            size = str(round(data.size/10**6, 2)).replace('.', ',')
            raise forms.ValidationError(f"Deine Datei ist mit {size} MB zu groß!",
                                        code='file_too_large')
        return data
