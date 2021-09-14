from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpRequest
from django.urls import reverse_lazy

from .models import Profile


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150, label="Vorname", widget=forms.TextInput(attrs={'class': "input"}))
    last_name = forms.CharField(max_length=150, label="Nachname", widget=forms.TextInput(attrs={'class': "input"}))
    picture = forms.ImageField(label="Profilbild", widget=forms.FileInput(attrs={'class': "file-input"}),
                               help_text="Dein Bild sollte bereits quadratisch zugeschnitten "
                                         "sein, da es sonst gestaucht dargestellt wird.")
    biography = forms.CharField(max_length=250, label="Biography", required=False,
                                widget=forms.Textarea(attrs={'class': "textarea", 'rows': "3"}))
    jobs = forms.CharField(max_length=100, label="Tätigkeiten", required=False,
                           widget=forms.TextInput(attrs={'class': "input"}),
                           help_text="Die Tätigkeiten müssen mittels Kommata getrennt angegeben werden.")
    course = forms.ChoiceField(choices=Profile.COURSES, label="Studiengang")
    degree = forms.ChoiceField(choices=Profile.DEGREES, label="Angestrebter Abschluss")
    birthday = forms.DateField(label="Geburtsdatum", required=False,
                               widget=forms.DateInput(attrs={'class': "input"}),
                               help_text="Das Datum ist nicht öffentlich einsehbar. An dein Geburtstag wird "
                                         "lediglich ein Kuchen in deinem öffentlichen Profil erscheinen.")
    joined_at = forms.DateField(label="Mitglied seit", widget=forms.DateInput(attrs={'class': "input"}))

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if data:
            if data >= date.today():
                raise ValidationError("Das Datum liegt in der Zukunft. Bitte wähle ein "
                                      "Datum, welches in der Vergangenheit liegt.")

        return data

    def clean_joined_at(self):
        data = self.cleaned_data['joined_at']
        if data:
            if data >= date.today():
                raise ValidationError("Das Datum liegt in der Zukunft. Bitte wähle ein "
                                      "Datum, welches in der Vergangenheit liegt.")

        return data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input"}),
            'last_name': forms.TextInput(attrs={'class': "input"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'username': forms.TextInput(attrs={'class': "input"}),
        }

    def send_email(self, request: HttpRequest, user: User, password: str):
        send_mail(
            "Deine Zugangsdaten für farafmb.de",
            f"""Hallo {user.first_name},

anbei findest du deine Zugangsdaten für {request.scheme}://{request.get_host()}

Benutzername:   {user.username}
Passwort:       {password}

Bitte ändere dein Passwort zeitnah unter: {request.scheme}://{request.get_host()}{reverse_lazy('admin:password_change')}

Viele Grüße
FaRaFMB
""",
            None,
            [user.email],
        )
