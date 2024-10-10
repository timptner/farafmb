from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from .forms import MentorForm
from .models import Registration, Program, Mentor


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        start = timezone.now()
        stop = start+ timedelta(days=30)
        self.registration = Registration.objects.create(name='Test', started_at=start, stopped_at=stop)
        self.program = Program.objects.create(name='Test')
        self.mentor = Mentor.objects.create(
            registration=self.registration,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.org',
            phone='+49123456789',
            program=self.program,
        )

    def test_landing_view(self):
        response = self.client.get('/mentoring/')
        self.assertEqual(response.status_code, 200)

    def test_mentor_list_view(self):
        response = self.client.get('/mentoring/mentor/')
        self.assertEqual(response.status_code, 302)

    def test_export_view(self):
        response = self.client.get('/mentoring/mentor/export')
        self.assertEqual(response.status_code, 301)

    def test_mentor_create_view(self):
        response = self.client.get('/mentoring/mentor/add/')
        self.assertEqual(response.status_code, 200)

    def test_mentor_create_done_view(self):
        response = self.client.get('/mentoring/mentor/add/done/')
        self.assertEqual(response.status_code, 200)

    def test_mentor_detail_view(self):
        response = self.client.get(f'/mentoring/mentor/{self.mentor.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_program_list_view(self):
        response = self.client.get('/mentoring/program/')
        self.assertEqual(response.status_code, 302)

    def test_program_create_view(self):
        response = self.client.get('/mentoring/program/add/')
        self.assertEqual(response.status_code, 302)

    def test_program_delete_view(self):
        response = self.client.get(f'/mentoring/program/{self.program.pk}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_registration_list_view(self):
        response = self.client.get('/mentoring/registration/')
        self.assertEqual(response.status_code, 302)

    def test_registration_create_view(self):
        response = self.client.get('/mentoring/registration/add/')
        self.assertEqual(response.status_code, 302)

    def test_registration_delete_view(self):
        response = self.client.get(f'/mentoring/registration/{self.registration.pk}/delete/')
        self.assertEqual(response.status_code, 302)


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
