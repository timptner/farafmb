from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone

from .models import Excursion


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        self.excursion = Excursion.objects.create(
            title='test',
            date=date(2050, 1, 1),
            seats=1,
            registration_ends_at=timezone.now() + timedelta(days=30),
        )

    def test_contact_form_view(self):
        response = self.client.get('/excursions/contact/')
        self.assertEqual(response.status_code, 302)

    def test_excursion_detail_view(self):
        response = self.client.get(f'/excursions/{self.excursion.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_registration_form_view(self):
        response = self.client.get(f'/excursions/{self.excursion.pk}/register/')
        self.assertEqual(response.status_code, 200)

    def test_registration_done_view(self):
        response = self.client.get(f'/excursions/{self.excursion.pk}/register/success/')
        self.assertEqual(response.status_code, 200)
