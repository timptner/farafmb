from django.test import TestCase
from django.shortcuts import reverse


class PublicViewsTest(TestCase):
    def test_news_view(self):
        response = self.client.get(reverse('blog:news'))
        self.assertEqual(response.status_code, 200)

    def test_archive_view(self):
        response = self.client.get(reverse('blog:archive'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        response = self.client.get(reverse('blog:contact'))
        self.assertEqual(response.status_code, 200)


class AdminViewsTest(TestCase):
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:posts'))
        self.assertEqual(response.status_code, 302)

    def test_post_create_view(self):
        response = self.client.get(reverse('blog:create-post'))
        self.assertEqual(response.status_code, 302)
