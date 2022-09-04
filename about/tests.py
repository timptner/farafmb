from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, RequestFactory

from .views import upload_file


class PublicViewsTest(SimpleTestCase):
    def test_about_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_upload_view(self):
        response = self.client.get('/about/upload/')
        self.assertEqual(response.status_code, 302)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='John', password='secret')

    def test_upload_view(self):
        request = self.factory.get('/about/upload/')
        request.user = self.user
        response = upload_file(request)
        self.assertEqual(response.status_code, 200)
