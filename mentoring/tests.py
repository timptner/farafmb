from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from .forms import MentorForm
from .models import Registration, Program, Mentor


class ProgramTestCase(TestCase):
    def setUp(self) -> None:
        Program.objects.create(name='Engineering')

    def test_program_has_display_name(self):
        """Display name of object corresponds to name field"""
        program = Program.objects.get()
        self.assertEqual(program.__str__(), program.name)


class MentorTestCase(TestCase):
    def setUp(self) -> None:
        start = timezone.now()
        stop = start + timedelta(days=30)
        registration = Registration.objects.create(name='Test', started_at=start, stopped_at=stop)
        Mentor.objects.create(registration=registration, first_name='John', last_name='Doe',
                              email='john.doe@example.org', phone='+491234567890')

    def test_full_name(self):
        """Full name consists of first and last name"""
        mentor = Mentor.objects.get()
        self.assertEqual(mentor.full_name, f"{mentor.first_name} {mentor.last_name}")

    def test_mentor_has_display_name(self):
        """Display name of object corresponds to name field"""
        mentor = Mentor.objects.get()
        self.assertEqual(mentor.__str__(), mentor.full_name)


class MentorFormTestCase(TestCase):
    def test_email_validation(self):
        """Mobile number is validated correctly"""
        form = MentorForm(data={'email': 'john.doe@st.ovgu.de'})  # valid
        self.assertNotIn('email', form.errors)

        form = MentorForm(data={'email': 'john.doe@example.org'})  # invalid host
        self.assertIn('email', form.errors)

    def test_phone_validation(self):
        """Mobile number is validated correctly"""
        form = MentorForm(data={'phone': '+49 123 4567890'})  # valid
        self.assertNotIn('phone', form.errors)

        form = MentorForm(data={'phone': '0049 123 4567890'})  # valid
        self.assertNotIn('phone', form.errors)

        form = MentorForm(data={'phone': '0123 4567890'})  # invalid country code
        self.assertIn('phone', form.errors)

        form = MentorForm(data={'phone': '+49 123 abc'})  # invalid values
        self.assertIn('phone', form.errors)
