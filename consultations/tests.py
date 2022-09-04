from datetime import time
from django.test import TestCase

from .utils import time_to_seconds, seconds_to_time, calc_max_step_size


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


class PublicViewsTest(TestCase):
    def test_consultation_views(self):
        response = self.client.get('/consultations/')
        self.assertEqual(response.status_code, 200)
