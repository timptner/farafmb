from django.test import TestCase


class PublicViewsTest(TestCase):
    def test_member_list_view(self):
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        response = self.client.get('/members/create/')
        self.assertEqual(response.status_code, 302)

    def test_user_profile_form_view(self):
        response = self.client.get('/members/update/')
        self.assertEqual(response.status_code, 302)
