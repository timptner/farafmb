from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext, gettext_lazy as _


class AuthenticationForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={'class': 'input', 'autofocus': True}))
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input', 'autocomplete': 'current-password'}),
    )
