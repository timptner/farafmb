from django.test import TestCase


class MemberListTest(TestCase):
    def test_member_list_view(self):
        response = self.client.get("/mitglieder/")
        self.assertEqual(response.status_code, 200)
