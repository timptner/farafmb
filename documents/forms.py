from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from pathlib import Path

from .models import Document


class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'file', 'visible')
        labels = {
            'title': _('Title'),
            'file': _('File'),
            'visible': _('Visible'),
        }
        help_texts = {
            'file': _('The file name will be changed to a URL-compliant version of the title after saving.'),
            'visible': _('This checkbox will only control if the file is listed on the documents view. The real '
                         'URL to the file itself will still be accessible.'),
        }

    def save(self, commit=True):
        form = super()
        obj = form.save(commit=False)
        if 'file' in form.changed_data:
            obj.file.name = slugify(obj.title) + Path(obj.file.name).suffix
        if commit:
            obj.save()
        return obj
