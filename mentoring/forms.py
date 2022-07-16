from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Registration, Program, Mentor, Helper


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'started_at', 'stopped_at', 'is_helper_form_active', 'helper_form_desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'E-Woche WS 2050'}),
            'started_at': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'stopped_at': forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'helper_form_desc': forms.Textarea(
                attrs={'class': 'textarea', 'rows': 5,
                       'placeholder': 'z. Bsp.: "Gebt eure gewünschte Station im Anmerkungsfeld ein.", "Nennt euren '
                                      'Partner für die Station im Anmerkungsfeld."'},
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get('started_at')
        stopped_at = cleaned_data.get('stopped_at')

        if started_at and stopped_at:
            # Stop before start
            if started_at >= stopped_at:
                raise ValidationError(_("Start date must be earlier than stop date"), code='invalid')

            registration_list = Registration.objects.all()

            for registration in registration_list:
                # Start inside another registration
                if registration.started_at <= started_at <= registration.stopped_at:
                    error_msg = ValidationError(_("The datetime is in the period of another registration."),
                                                code='invalid')
                    self.add_error('started_at', error_msg)

                # Stop inside another registration
                if registration.started_at <= stopped_at <= registration.stopped_at:
                    error_msg = ValidationError(_("The datetime is in the period of another registration."),
                                                code='invalid')
                    self.add_error('stopped_at', error_msg)

            # Another registration between start and stop
            is_between = Registration.objects.filter(started_at__gte=started_at, stopped_at__lte=stopped_at).exists()
            if is_between:
                raise ValidationError(_("Another registration is between the start and end of this registration."),
                                      code='invalid')


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
        }


class MentorForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True, label=_("Privacy"))

    class Meta:
        model = Mentor
        fields = ['first_name', 'last_name', 'email', 'phone', 'program']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Maxi'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Mustermensch'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'maxi.mustermensch@st.ovgu.de'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': '+49 123 4567890'}),
        }
        help_texts = {
            'email': _("Only email addresses from Otto von Guericke University Magdeburg are allowed."),
            'phone': _("Write your mobile number, starting with the country code.")
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if 'class' in visible.field.widget.attrs:
                cls_list = visible.field.widget.attrs['class'].split()
            else:
                cls_list = []
            if visible._has_changed():
                cls_list.append('is-danger') if visible.errors else cls_list.append('is-success')
            visible.field.widget.attrs['class'] = ' '.join(cls_list)

    def clean_email(self):
        data = self.cleaned_data['email']

        username, host = data.split('@')
        if host not in ['st.ovgu.de', 'ovgu.de']:
            raise ValidationError(_("Your email address does not belong to Otto von Guericke University Magdeburg."),
                                  code='blocked')

        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']

        data = ''.join(data.split())  # Remove all whitespace

        if data.startswith('00'):
            data = data.replace('00', '+', 1)  # Replace leading zeros with plus symbol (country code)

        if not data.startswith('+'):
            raise ValidationError(_("Your mobile number does not start with a country code."), code='faulty')

        if not all([item.isdigit() for item in data[1:]]):
            raise ValidationError(_("Your mobile number contains non-numeric values."), code='invalid')

        return data


class HelperForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True, label=_("Privacy"))

    class Meta:
        model = Helper
        fields = ['first_name', 'last_name', 'email', 'phone', 'comment']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Maxi'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Mustermensch'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'maxi.mustermensch@st.ovgu.de'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': '+49 123 4567890'}),
            'comment': forms.Textarea(attrs={'class': 'textarea', 'rows': 5}),
        }
        help_texts = {
            'email': _("Only email addresses from Otto von Guericke University Magdeburg are allowed."),
            'phone': _("Write your mobile number, starting with the country code.")
        }

    def clean_email(self):
        data = self.cleaned_data['email']

        username, host = data.split('@')
        if host not in ['st.ovgu.de', 'ovgu.de']:
            raise ValidationError(
                _("Your email address does not belong to Otto von Guericke University Magdeburg."),
                code='blocked')

        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']

        data = ''.join(data.split())  # Remove all whitespace

        if data.startswith('00'):
            data = data.replace('00', '+', 1)  # Replace leading zeros with plus symbol (country code)

        if not data.startswith('+'):
            raise ValidationError(_("Your mobile number does not start with a country code."), code='faulty')

        if not all([item.isdigit() for item in data[1:]]):
            raise ValidationError(_("Your mobile number contains non-numeric values."), code='invalid')

        return data
