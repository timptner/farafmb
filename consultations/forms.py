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
        day = cleaned_data.get('day')
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end:
            if start >= end:
                msg = _("Start of consultation must be earlier then its end.")
                self.add_error('start', msg)
                self.add_error('end', msg)

        if day and start and end:
            # Validate start is not between another consultation
            if Consultation.objects.filter(day=day, start__lt=start, end__gt=start).exists():
                self.add_error('start', _("Value is between another consultation."))

            # Validate end is not between another consultation
            if Consultation.objects.filter(day=day, start__lt=end, end__gt=end).exists():
                self.add_error('end', _("Value is between another consultation."))

            # Validate no other consultation is between start and end
            if Consultation.objects.filter(day=day, start__gte=start, end__lte=end).exists():
                msg = _("Another consultation is between this consultation.")
                self.add_error('start', msg)
                self.add_error('end', msg)
