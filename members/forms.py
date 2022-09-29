from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from farafmb import forms

from .models import Member


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


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['picture', 'biography', 'jobs', 'course', 'degree', 'birthday', 'joined_at']
        labels = {
            'birthday': _("Birthday (Optional)"),
        }
        widgets = {
            'picture': forms.FileInput(),
            'biography': forms.Textarea(attrs={'rows': 3}),
            'jobs': forms.TextInput(),
            'course': forms.Select(),
            'degree': forms.Select(),
            'birthday': forms.DateInput(),
            'joined_at': forms.DateInput(),
        }
        help_texts = {
            'picture': _("Leave this field blank if you do not want to change your image."),
            'biography': _("A maximum length of 250 characters are allowed."),
            'jobs': _("You can separate multiple jobs with a comma."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial:
            self.initial['birthday'] = self.instance.birthday.isoformat() if self.initial['birthday'] else ''
            self.initial['joined_at'] = self.instance.joined_at.isoformat() if self.initial['joined_at'] else ''

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if data:
            if data >= timezone.now().date():
                raise ValidationError(_("You can only choose a date in the past."))

        return data

    def clean_joined_at(self):
        data = self.cleaned_data['joined_at']
        if data >= timezone.now().date():
            raise ValidationError(_("You can only choose a date in the past."))

        return data
