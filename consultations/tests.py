from datetime import time

from django.test import TestCase


class PublicViewsTest(TestCase):
    def test_consultation_views(self):
        response = self.client.get('/consultations/')
        self.assertEqual(response.status_code, 200)
