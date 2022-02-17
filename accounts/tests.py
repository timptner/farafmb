from django.test import TestCase
from django.urls import reverse


class ViewsTest(TestCase):
    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        url = reverse('logout')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_password_change_view(self):
        url = reverse('password_change')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_password_change_done_view(self):
        url = reverse('password_change_done')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_password_reset_view(self):
        url = reverse('password_reset')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_view(self):
        url = reverse('password_reset_done')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_view(self):
        url = reverse('password_reset_confirm', args=['test', 'test'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_view(self):
        url = reverse('password_reset_complete')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
