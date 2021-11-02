import secrets

from django import forms
from django.core.exceptions import ValidationError

from .models import Job, Document


class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('slug'):
            self.fields['slug'].disabled = True
            self.fields['slug'].help_text = "Dieses Feld kann nicht verändert werden. " \
                                            "Bitte wende dich ggf. an den Administrator."
        else:
            self.fields['slug'].help_text = "Dieses Feld kann nachträglich nicht mehr verändert werden."

    class Meta:
        model = Job
        fields = ('title', 'slug', 'desc', 'file', 'expired_on')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('job', 'title', 'file')

    def clean_file(self):
        data = self.cleaned_data['file']
        if not data.name.endswith('.pdf'):
            raise ValidationError("Es sind nur Dokumente des Datei-Typs PDF erlaubt.")
        data.name = secrets.token_urlsafe(5) + '.pdf'
        return data
