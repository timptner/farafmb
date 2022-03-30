import re

from django import forms
from django.forms.renderers import TemplatesSetting
from django.utils.translation import gettext_lazy as _

from .models import Participant, Event


class ParticipantForm(forms.ModelForm):
    default_renderer = TemplatesSetting
    privacy = forms.BooleanField(label=_("Privacy"),
                                 widget=forms.CheckboxInput(attrs={
                                     'data-label': _("I accept the privacy statement and agree to "
                                                     "the processing of my personal data."),
                                 }))

    class Meta:
        model = Participant
        fields = ('event', 'first_name', 'last_name', 'email', 'comment')
        help_texts = {
            'email': _("Only email addresses with the domain 'st.ovgu.de' are allowed."),
        }
        widgets = {
            'event': forms.HiddenInput(),
        }

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        if not re.match(r'^([^@]*)@((st\.)?ovgu\.de)$', data):
            raise forms.ValidationError(_("Please use your university email address. "
                                          "(Did you even read the help text above? 🧐)"),
                                        code='forbidden_email')
        return data

    def save(self, commit=True):
        form = super()
        obj: Event = form.save(commit=False)
        if commit:
            obj.save()
        return obj
