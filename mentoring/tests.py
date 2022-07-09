from django.test import TestCase

from .models import Program, Mentor


class ProgramTestCase(TestCase):
    def setUp(self) -> None:
        Program.objects.create(faculty=Program.Faculties.FMB, name='Engineering')

    def test_program_has_display_name(self):
        """Display name of object corresponds to name field"""
        program = Program.objects.get()
        self.assertEqual(program.__str__(), program.name)


class MentorTestCase(TestCase):
    def setUp(self) -> None:
        Mentor.objects.create(first_name='John', last_name='Doe', email='john.doe@example.org', phone='+491234567890')

    def test_full_name(self):
        """Full name consists of first and last name"""
        mentor = Mentor.objects.get()
        self.assertEqual(mentor.full_name, f"{mentor.first_name} {mentor.last_name}")

    def test_mentor_has_display_name(self):
        """Display name of object corresponds to name field"""
        mentor = Mentor.objects.get()
        self.assertEqual(mentor.__str__(), mentor.full_name)
