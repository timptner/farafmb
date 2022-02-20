from datetime import timedelta
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase, override_settings, RequestFactory
from django.urls import reverse
from django.utils import timezone
from farafmb.utils import human_bytes
from unittest.mock import patch

from .admin import ExamAdmin
from .forms import SubmitForm, MAX_FILE_SIZE
from .models import Exam


class ExamTests(TestCase):
    def test_course_represents_instance(self):
        exam = Exam.objects.create(course='Test course', date=timezone.localdate())
        self.assertEqual(str(exam), exam.course)


class ExamAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='john', email='john@admin.org', password='secret')

    def test_remove_minute_author(self):
        admin = ExamAdmin(Exam, self.site)
        request = self.factory.get(reverse('admin:exams_exam_changelist'))
        request.user = self.user

        # required when using messages
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        exam = Exam.objects.create(course='Some course', minute_author='test@example.org', date=timezone.localdate())
        admin.remove_minute_author(request, Exam.objects.all())
        exam.refresh_from_db()

        self.assertIsNone(exam.minute_author)


@override_settings(LANGUAGE_CODE='en-us')
class SubmitFormTests(TestCase):
    def setUp(self) -> None:
        self.valid_data = {
            'privacy': True,
            'course': 'Some cool new stuff',
            'lecturer': 'A lame dude',
            'date': timezone.localdate(),
            'minute_author': 'student@st.ovgu.de',
        }
        self.file_data = {'minute_file': SimpleUploadedFile('file.pdf', b'Some content')}

    @patch('django.core.files.storage.FileSystemStorage._save')
    def test_valid_form(self, mock_save):
        mock_save.return_value = 'file.pdf'
        data = self.valid_data
        form = SubmitForm(data, self.file_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertFalse('privacy' in dir(instance))
        self.assertEqual(instance.course, data['course'])
        self.assertEqual(instance.lecturer, data['lecturer'])
        self.assertEqual(instance.date, data['date'])
        self.assertEqual(instance.minute_author, data['minute_author'])
        self.assertEqual(instance.minute_file, self.file_data['minute_file'])

    @patch('django.core.files.storage.FileSystemStorage._save')
    def test_date_is_future(self, mock_save):
        mock_save.return_value = 'file.pdf'
        data = self.valid_data
        data['date'] = timezone.localdate() + timedelta(days=1)
        form = SubmitForm(data, self.file_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ["The date can't be in the future. (Are you a time traveler? 🧙)"])

    @patch('django.core.files.storage.FileSystemStorage._save')
    def test_email_is_not_allowed(self, mock_save):
        mock_save.return_value = 'file.pdf'
        data = self.valid_data
        data['minute_author'] = 'student@example.org'
        form = SubmitForm(data, self.file_data)
        self.assertFalse(form.is_valid())
        self.assertIn('minute_author', form.errors)
        self.assertEqual(form.errors['minute_author'], ["Please use your university email address. "
                                                        "(Did you even read the help text above? 🧐)"])

    @patch('django.core.files.storage.FileSystemStorage._save')
    @patch('django.core.files.uploadedfile.SimpleUploadedFile', spec=SimpleUploadedFile)
    def test_file_size_is_above_limit(self, mock_save, mock_file):
        mock_save.return_value = 'file.pdf'
        mock_file().size = 10_000_000  # Byte
        data = self.file_data
        data['minute_file'] = mock_file()
        form = SubmitForm(self.valid_data, data)
        self.assertFalse(form.is_valid())
        self.assertIn('minute_file', form.errors)
        self.assertEqual(form.errors['minute_file'], ["Your file size (%(size)s) is above the allowed maximum of "
                                                      "%(max_size)s." % {'size': human_bytes(data['minute_file'].size),
                                                                         'max_size': human_bytes(MAX_FILE_SIZE)}])


@override_settings(LANGUAGE_CODE='en-us')
class ViewTests(SimpleTestCase):
    def test_info(self):
        url = reverse('exams:info')
        self.assertEqual(url, '/exams/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Memory minutes')

    def test_submit(self):
        url = reverse('exams:submit')
        self.assertEqual(url, '/exams/submit/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit your memory minutes')

    def test_submit_done(self):
        url = reverse('exams:submit_done')
        self.assertEqual(url, '/exams/submit/done/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success')
