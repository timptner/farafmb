from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, RequestFactory
from django.utils import translation

from .forms import PasswordResetForm


class AuthViewsTest(TestCase):
    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)


class PasswordViewsTest(TestCase):
    def test_password_change_view(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 302)

    def test_password_reset_view(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_view(self):
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_view(self):
        response = self.client.get('/accounts/reset/test_id/test_token/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_view(self):
        response = self.client.get('/accounts/reset/done/')
        self.assertEqual(response.status_code, 200)


class ResetEmailTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='john',
            email='john@example.org',
            password='secret',
        )

    def test_send_reset_email_with_user(self) -> None:
        request = self.factory.post('/accounts/password_reset/')
        form = PasswordResetForm(data={'username': 'john'})
        form.full_clean()
        form.save(request=request)
        self.assertEqual(len(mail.outbox), 1)

    def test_send_reset_email_with_domain(self) -> None:
        domain = 'example.org'
        request = self.factory.post('/accounts/password_reset/')
        with translation.override('en'):
            form = PasswordResetForm(data={'username': 'john'})
            form.full_clean()
            form.save(domain_override=domain, request=request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"Password reset on {domain}")

    def test_send_reset_email_without_user(self) -> None:
        request = self.factory.post('/accounts/password_reset/')
        form = PasswordResetForm(data={'username': 'anonymous'})
        form.full_clean()
        form.save(request=request)
        self.assertEqual(len(mail.outbox), 0)
