from django.contrib.auth import views as auth_views

from . import forms


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = forms.AuthenticationForm


class LogoutView(auth_views.LogoutView):
    pass


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = forms.PasswordChangeForm


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    form_class = forms.PasswordResetForm


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass
