from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from farafmb import forms

from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['day', 'start', 'end', 'text']
        widgets = {
            'day': forms.Select(),
            'start': forms.TimeInput(),
            'end': forms.TimeInput(),
        }

    def clean_start(self):
        data = self.cleaned_data['start']
        valid_hours = range(7, 20)
        if data.hour not in valid_hours:
            raise ValidationError(
                _("Only hours between %(min)s and %(max)s are allowed."),
                params={
                    'min': min(valid_hours),
                    'max': max(valid_hours),
                }
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end:
            if start >= end:
                msg = _("Start of consultation must be earlier then its end.")
                self.add_error('start', msg)
                self.add_error('end', msg)
