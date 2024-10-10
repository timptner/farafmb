from django.test import TestCase
from django.urls import reverse


class PublicViewsTest(TestCase):
    def test_member_list_view(self):
        response = self.client.get(reverse('members:member-list'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        response = self.client.get(reverse('members:user-create'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_form_view(self):
        response = self.client.get(reverse('members:member-create'))
        self.assertEqual(response.status_code, 302)
