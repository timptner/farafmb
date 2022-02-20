import shutil
import tempfile

from datetime import date
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from http import HTTPStatus
from farafmb.utils import generate_random_file_name

from .forms import ExamSubmitForm
from .models import Exam

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ExamTest(TestCase):
    def setUp(self) -> None:
        pdf_file = File(SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'),
                        name=generate_random_file_name(suffix='.pdf'))
        self.exam = Exam.objects.create(course='Astrophysics', lecturer='Tyson', date=date(2022, 1, 1),
                                        minute_author='John', minute_file=pdf_file)

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_object_name(self):
        """Object is represented by its course."""
        self.assertEqual(str(self.exam), self.exam.course)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ExamSubmitFormTest(TestCase):
    def tearDown(self) -> None:
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_form_data_is_valid(self):
        """
        Valid form data is passed.
        """
        data = {
            'privacy': "yes",
            'course': "Some course",
            'lecturer': "Some lecturer",
            'date': "2000-01-01",
            'minute_author': "student@st.ovgu.de",
        }
        files = {
            'minute_file': SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'),
        }
        form = ExamSubmitForm(data=data, files=files)
        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertEqual(obj, Exam.objects.get(course="Some course"))

    def test_form_data_is_invalid(self):
        """
        Invalid form data raised a ValidationError.
        """
        data = {
            'privacy': "yes",
            'course': "Some course",
            'lecturer': "Some lecturer",
            'date': "9999-12-31",
            'minute_author': "student@example.org",
        }
        file = SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf')
        setattr(file, 'size', 10 * 10 ** 10)
        files = {
            'minute_file': file,
        }
        form = ExamSubmitForm(data, files=files)
        self.assertFalse(form.is_valid())
        self.assertTrue('date' in form.errors)
        self.assertTrue('minute_author' in form.errors)
        self.assertTrue('minute_file' in form.errors)


class SubmitExamViewTest(TestCase):
    def test_get(self):
        """
        Views respond a GET request with http status OK.
        """
        routes = {
            'exams:info': '/exams/',
            'exams:submit': '/exams/submit/',
            'exams:submit_done': '/exams/submit/done/',
        }
        for key, value in routes.items():
            url = reverse(key)
            self.assertEqual(url, value)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_success(self):
        """
        Views respond a valid POST request with http status FOUND.
        """
        data = {
            'privacy': "yes",
            'course': "Some course",
            'lecturer': "Some lecturer",
            'date': "2000-01-01",
            'minute_author': "student@st.ovgu.de",
            'minute_file': SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'),
        }
        response = self.client.post('/exams/submit/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response['Location'], '/exams/submit/done/')

    def test_post_error(self):
        """
        Views respond an invalid POST request with http status OK.
        """
        data = {
            'privacy': "yes",
            'course': "Some course",
            'lecturer': "Some lecturer",
            'date': "9999-12-31",
            'minute_author': "student@example.org",
            'minute_file': SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'),
        }
        response = self.client.post('/exams/submit/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
