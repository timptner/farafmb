from django.test import TestCase


class PublicViewsTest(TestCase):
    def test_job_list_view(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)
