from datetime import date
from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150, label="Vorname", widget=forms.TextInput(attrs={'class': "input"}))
    last_name = forms.CharField(max_length=150, label="Nachname", widget=forms.TextInput(attrs={'class': "input"}))
    picture = forms.ImageField(label="Profilbild", widget=forms.FileInput(attrs={'class': "file-input"}),
                               help_text="Die Datei wird nach dem Speichern automatisch "
                                         "in einen zufällig generierten Schlüssel umbenannt.")
    biography = forms.CharField(max_length=250, label="Biography", required=False,
                                widget=forms.Textarea(attrs={'class': "textarea", 'rows': "3"}))
    jobs = forms.CharField(max_length=100, label="Tätigkeiten", required=False,
                           widget=forms.TextInput(attrs={'class': "input"}),
                           help_text="Die Tätigkeiten müssen mittels Kommata getrennt angegeben werden.")
    course = forms.ChoiceField(choices=Profile.COURSES, label="Studiengang")
    birthday = forms.DateField(label="Geburtsdatum", required=False,
                               widget=forms.DateInput(attrs={'class': "input"}),
                               help_text="Das Datum ist nicht öffentlich einsehbar. An dein Geburtstag wird "
                                         "lediglich ein Kuchen in deinem öffentlichen Profil erscheinen.")

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if data:
            if data >= date.today():
                raise ValidationError("Das Datum liegt in der Zukunft. Bitte wähle ein "
                                      "Datum, welches in der Vergangenheit liegt.")

        return data
