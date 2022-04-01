from datetime import timedelta
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import ParticipantForm
from .models import Event, Participant


class EventTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(title="Test", desc="Lorem ipsum")

        tomorrow = timezone.now() + timedelta(days=1)
        self.upcoming_event = Event.objects.create(title="Test", desc="Lorem ipsum", registration_started_at=tomorrow)

        yesterday = timezone.now() - timedelta(days=1)
        self.past_event = Event.objects.create(title="Test", desc="Lorem ipsum", registration_stopped_at=yesterday)

    def test_representation(self):
        self.assertEqual(str(self.event), self.event.title)

    def test_absolute_url(self):
        url = reverse('events:info', kwargs={'pk': self.event.pk})
        self.assertEqual(self.event.get_absolute_url(), url)

    def test_registration_status(self):
        self.assertEqual(self.event.registration_status(), 'open')
        self.assertEqual(self.upcoming_event.registration_status(), 'pending')
        self.assertEqual(self.past_event.registration_status(), 'closed')

    def test_registration_is_closed(self):
        self.assertFalse(self.event.registration_is_closed())
        self.assertTrue(self.past_event.registration_is_closed())
        self.assertTrue(self.upcoming_event.registration_is_closed())


class ParticipantTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(title="Test", desc="Lorem ipsum")
        self.participant = Participant.objects.create(event=self.event, first_name="John", last_name="Doe",
                                                      email="user@example.org", comment="Hello World")

    def test_representation(self):
        self.assertEqual(str(self.participant), self.participant.full_name())

    def test_full_name(self):
        self.assertEqual(self.participant.full_name(), f"{self.participant.first_name} {self.participant.last_name}")


@override_settings(LANGUAGE_CODE='en-us')
class ParticipantFormTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(title="Test", desc="Lorem ipsum")
        self.valid_data = {
            'event': self.event.pk,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@st.ovgu.de',
            'comment': 'Hello World',
            'privacy': True,
        }

    def test_valid_form(self):
        data = self.valid_data
        form = ParticipantForm(data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.event.pk, data['event'])
        self.assertEqual(instance.first_name, data['first_name'])
        self.assertEqual(instance.last_name, data['last_name'])
        self.assertEqual(instance.email, data['email'])
        self.assertEqual(instance.comment, data['comment'])
        self.assertFalse('privacy' in dir(instance))

    def test_not_allowed_email(self):
        data = self.valid_data
        data['email'] = 'user@example.org'
        form = ParticipantForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Please use your university email address. "
                                                "(Did you even read the help text above? 🧐)"])


class RegistrationViewTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(title="Test", desc="Lorem ipsum")

        tomorrow = timezone.now() + timedelta(days=1)
        self.upcoming_event = Event.objects.create(title="Test", desc="Lorem ipsum", registration_started_at=tomorrow)

        yesterday = timezone.now() - timedelta(days=1)
        self.past_event = Event.objects.create(title="Test", desc="Lorem ipsum", registration_stopped_at=yesterday)

    def test_registration_forbidden(self):
        url = reverse('events:registration', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('events:registration', kwargs={'pk': self.upcoming_event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('events:registration', kwargs={'pk': self.past_event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)


@override_settings(LANGUAGE_CODE='en-us')
class ViewTests(TestCase):
    def setUp(self) -> None:
        self.event = Event.objects.create(title="Test", desc="Lorem ipsum")

    def test_info(self):
        url = reverse('events:info', kwargs={'pk': self.event.pk})
        self.assertEqual(url, f'/events/{self.event.pk}/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

    def test_registration(self):
        url = reverse('events:registration', kwargs={'pk': self.event.pk})
        self.assertEqual(url, f'/events/{self.event.pk}/register/')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registration for event')

    def test_registration_done(self):
        url = reverse('events:registration_done', kwargs={'pk': self.event.pk})
        self.assertEqual(url, f'/events/{self.event.pk}/register/done/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success')
