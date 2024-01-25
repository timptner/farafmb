from django.test import SimpleTestCase


class PublicViewsTest(SimpleTestCase):
    def test_about_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
