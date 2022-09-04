from django.test import TestCase


class PublicViewsTest(TestCase):
    def test_posts_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_exams_redirect(self):
        response = self.client.get('/protocols/')
        self.assertEqual(response.status_code, 301)
