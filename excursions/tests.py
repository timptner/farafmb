from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from excursions.models import Excursion


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        self.excursion = Excursion.objects.create(
            title='test',
            date=date(2050, 1, 1),
            seats=1,
            registration_ends_at=timezone.now() + timedelta(days=30),
        )

    def test_contact_form_view(self):
        response = self.client.get(reverse('excursions:contact'))
        self.assertEqual(response.status_code, 302)
