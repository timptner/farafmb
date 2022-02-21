from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse

from .admin import LinkAdmin
from .models import Link


class LinkTests(TestCase):
    def test_object_representation(self):
        link = Link.objects.create(url='https://www.example.org', text='Example', position=1)
        self.assertEqual(str(link), link.text)


class LinkAdminTests(TestCase):
    def setUp(self) -> None:
        site = AdminSite()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='john', email='john@example.org', password='secret')
        self.admin = LinkAdmin(Link, site)

    def test_initial_data(self):
        request = self.factory.get(reverse('admin:links_link_changelist'))
        request.user = self.user
        initial_data = self.admin.get_changeform_initial_data(request)
        self.assertEqual(initial_data, {'icon': 'fas fa-link'})

    def test_mark_as_active_action(self):
        request = self.factory.get(reverse('admin:links_link_changelist'))
        request.user = self.user

        # Required when using messages in action
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        Link.objects.bulk_create([
            Link(url='https://www.example1.org', text='Example 1', position=1, is_active=False),
            Link(url='https://www.example2.org', text='Example 2', position=2, is_active=False),
            Link(url='https://www.example2.org', text='Example 3', position=3, is_active=False),
        ])
        queryset = Link.objects.all()
        self.admin.mark_as_active(request, queryset)
        for link in queryset:
            self.assertTrue(link.is_active)

    def test_mark_as_inactive_action(self):
        request = self.factory.get(reverse('admin:links_link_changelist'))
        request.user = self.user

        # Required when using messages in action
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        Link.objects.bulk_create([
            Link(url='https://www.example1.org', text='Example 1', position=1, is_active=True),
            Link(url='https://www.example2.org', text='Example 2', position=2, is_active=True),
            Link(url='https://www.example2.org', text='Example 3', position=3, is_active=True),
        ])
        queryset = Link.objects.all()
        self.admin.mark_as_inactive(request, queryset)
        for link in queryset:
            self.assertFalse(link.is_active)


@override_settings(LANGUAGE_CODE='en-us')
class LinkViewTests(TestCase):
    def test_index(self):
        url = reverse('links:index')
        self.assertEqual(url, '/links/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
