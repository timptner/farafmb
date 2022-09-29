from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from farafmb import forms

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
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'username': forms.TextInput(),
        }
        help_texts = {
            'username': _("Preferably, use the first name as the user name. If this is already taken, add a few "
                          "letters from the beginning of the last name to the end."),
        }

            f"""Hallo {user.first_name},
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    def clean_email(self):
        data = self.cleaned_data['email']
        username, domain = data.split('@')
        if domain not in ['ovgu.de', 'st.ovgu.de']:
            raise ValidationError(_("Only domains of Otto von Guericke University are allowed."))

        return data

    def send_email(self, user, request):
        token_generator = PasswordResetTokenGenerator()

        context = {
            'first_name': self.cleaned_data['first_name'],
            'username': self.cleaned_data['username'],
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
        body = loader.render_to_string('members/password_mail.txt', context)

        send_mail(
            subject=_("Set your password"),
            message=body,
            from_email=None,
            recipient_list=[self.cleaned_data['email']],
        )


