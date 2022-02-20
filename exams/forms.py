import re

from django import forms
from django.forms.renderers import TemplatesSetting
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from farafmb.utils import generate_random_file_name, human_bytes
from pathlib import Path

from .models import Exam

MAX_FILE_SIZE = 2_000_000  # Byte


class SubmitForm(forms.ModelForm):
    default_renderer = TemplatesSetting
    privacy = forms.BooleanField(label=_('Privacy'),
                                 widget=forms.CheckboxInput(attrs={
                                     'data-label': _("I accept the privacy statement and agree to "
                                                     "the processing of my personal data."),
                                 }))

    class Meta:
        model = Exam
        fields = ('course', 'lecturer', 'date', 'minute_author', 'minute_file')
        labels = {
            'course': _("Course"),
            'lecturer': _("Lecturer"),
            'date': _("Date of the exam"),
            'minute_author': _("Author of the minute"),
            'minute_file': _("Minute file"),
        }
        help_texts = {
            'minute_author': _("Only email addresses with the domain 'st.ovgu.de' are allowed."),
            'minute_file': _("Only PDF files with a maximum size "
                             "of %s can be submitted.") % human_bytes(MAX_FILE_SIZE),
        }

    def clean_date(self):
        data = self.cleaned_data['date']
        if data > timezone.localdate():
            raise forms.ValidationError(_("The date can't be in the future. (Are you a time traveler? 🧙)"),
                                        code='future_date')
        return data

    def clean_minute_author(self):
        data = self.cleaned_data['minute_author'].lower()
        if not re.match(r'^([^@]*)@((st\.)?ovgu\.de)$', data):
            raise forms.ValidationError(_("Please use your university email address. "
                                          "(Did you even read the help text above? 🧐)"),
                                        code='forbidden_email')
        return data

    def clean_minute_file(self):
        data = self.cleaned_data['minute_file']
        if data.size > MAX_FILE_SIZE:
            raise forms.ValidationError(_("Your file size (%(size)s) is above the allowed maximum of "
                                          "%(max_size)s.") % {'size': human_bytes(data.size),
                                                              'max_size': human_bytes(MAX_FILE_SIZE)},
                                        code='file_size_too_large')
        return data

    def save(self, commit=True):
        form = super()
        obj: Exam = form.save(commit=False)
        file = obj.minute_file
        if 'minute_file' in form.changed_data:
            file.name = generate_random_file_name(suffix=Path(file.name).suffix)
        if commit:
            obj.save()
        return obj
