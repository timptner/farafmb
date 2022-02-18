from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from pathlib import Path

from .models import Document


class DocumentAdminForm(forms.ModelForm):
    file = forms.FileField(help_text=_('The file name will be changed to a URL-compliant '
                                       'version of the title after saving.'))

    class Meta:
        model = Document
        fields = ('title', 'file', 'visible')

    def save(self, commit=True):
        form = super()
        obj = form.save(commit=False)
        if 'file' in form.changed_data:
            obj.file.name = slugify(obj.title) + Path(obj.file.name).suffix
        if commit:
            obj.save()
        return obj
