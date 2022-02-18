import shutil
import tempfile

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils.text import slugify
from pathlib import Path

from .forms import DocumentAdminForm
from .models import Document

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class DocumentTestCase(TestCase):
    def setUp(self):
        pdf_file = File(SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'), name='file.pdf')
        Document.objects.create(title='My custom file', file=pdf_file)
        zip_file = File(SimpleUploadedFile('File.zip', b'content', content_type='application/zip'), name='file.zip')
        Document.objects.create(title='My custom archive', file=zip_file)
        txt_file = File(SimpleUploadedFile('File.txt', b'content', content_type='text/plain'), name='file.txt')
        Document.objects.create(title='My custom file', file=txt_file)

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_file_extension_recognized(self):
        """File extensions are correctly identified"""
        pdf_document = Document.objects.get(file='documents/file.pdf')
        zip_document = Document.objects.get(file='documents/file.zip')
        txt_document = Document.objects.get(file='documents/file.txt')
        self.assertEqual(pdf_document.file_suffix(), '.pdf')
        self.assertEqual(zip_document.file_suffix(), '.zip')
        self.assertEqual(txt_document.file_suffix(), '.txt')

    def test_icon_switch_case(self):
        """Check for all possible icons shown"""
        pdf_document = Document.objects.get(file='documents/file.pdf')
        zip_document = Document.objects.get(file='documents/file.zip')
        txt_document = Document.objects.get(file='documents/file.txt')
        self.assertEqual(pdf_document.icon(), 'fas fa-file-pdf')
        self.assertEqual(zip_document.icon(), 'fas fa-file-archive')
        self.assertEqual(txt_document.icon(), 'fas fa-file')

    def test_object_name(self):
        """Check if object is represented by its title"""
        pdf_document = Document.objects.get(file='documents/file.pdf')
        self.assertEqual(str(pdf_document), pdf_document.title)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class AddDocumentAdminFormTestCase(TestCase):
    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_admin_form_saved(self):
        """Form gets properly saved with file name set from title"""
        title = 'My special document'
        file = File(SimpleUploadedFile('File.pdf', b'content', content_type='application/pdf'), name='file.pdf')
        form = DocumentAdminForm(data={'title': title}, files={'file': file})
        obj = form.save()
        self.assertEqual(obj.title, title)
        self.assertEqual(obj.file.name, Document.file.field.upload_to + slugify(title) + Path(file.name).suffix)
