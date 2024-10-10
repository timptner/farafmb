from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.test import override_settings, RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from links.admin import LinkAdmin
from links.forms import ChangeOrderForm
from links.models import Link
from links.views import change_order


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


class LinkViewTests(TestCase):
    def test_index(self):
        url = reverse('links:index')
        self.assertEqual(url, '/links/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(LANGUAGE_CODE='en-us')
class ChangeOrderFormTests(TestCase):
    def test_clean_order_valid(self):
        form = ChangeOrderForm({'order': '4,8,15,16,23,42'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['order'], [4, 8, 15, 16, 23, 42])

    def test_clean_order_invalid(self):
        form = ChangeOrderForm({'order': '4,8,x,23,42'})
        self.assertFalse(form.is_valid())
        self.assertIn('order', form.errors)
        self.assertEqual(form.errors['order'], ["Not all positions are integers."])

    def test_save(self):
        link1 = Link.objects.create(position=0)
        link2 = Link.objects.create(position=1)
        link3 = Link.objects.create(position=2)
        order = f'{link3.pk},{link2.pk},{link1.pk}'
        form = ChangeOrderForm({'order': order})
        self.assertTrue(form.is_valid())
        form.save()
        link1.refresh_from_db()
        self.assertEqual(link1.position, 2)
        link2.refresh_from_db()
        self.assertEqual(link2.position, 1)
        link3.refresh_from_db()
        self.assertEqual(link3.position, 0)


class ChangeOrderViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='John', email='john@example.org', password='secret')

    def test_change_order(self):
        url = reverse('links:change_order')
        self.assertEqual(url, '/links/change_order/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_change_order_get(self):
        request = self.factory.get('links:change_order')
        request.user = self.user
        response = change_order(request)
        self.assertEqual(response.status_code, 200)

    def test_change_order_post(self):
        link = Link.objects.create()
        request = self.factory.post('links:change_order')
        request.user = self.user
        request.POST = {'order': f'{link.pk}'}
        response = change_order(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], reverse('links:change_order_done'))


class ChangeOrderDoneViewTests(SimpleTestCase):
    def test_change_order_done(self):
        url = reverse('links:change_order_done')
        self.assertEqual(url, '/links/change_order/done/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
