from django.contrib.auth import views as auth_views

from . import forms


class LoginView(auth_views.LoginView):
    form_class = forms.AuthenticationForm


class LogoutView(auth_views.LogoutView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    form_class = forms.PasswordResetForm
