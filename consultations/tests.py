from datetime import time
from django.test import TestCase, RequestFactory

from .utils import time_to_seconds, seconds_to_time, calc_max_step_size
from .views import ConsultationsView


class UtilityTestCase(TestCase):
    def test_time_to_seconds(self):
        """Time is correctly converted total seconds"""
        self.assertEqual(time_to_seconds(time(12)), 12 * 60 * 60)

    def test_seconds_to_time(self):
        """Total seconds are correctly converted to time"""
        self.assertEqual(seconds_to_time(12 * 60 * 60), time(12))

    def test_calc_max_step_size(self):
        """GCD is calculated correctly"""
        self.assertEqual(calc_max_step_size([time(12), time(13, 30), time(14)]), 1800)


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_views(self):
        """Check for dead links"""
        request = self.factory.get('/consultations/')
        response = ConsultationsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
