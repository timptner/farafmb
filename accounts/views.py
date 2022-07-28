from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import forms


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = forms.AuthenticationForm


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = forms.PasswordResetForm
    email_template_name = 'accounts/password_reset_mail.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = forms.SetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('accounts:password_change')
    success_message = _("Your password has been changed successfully.")
