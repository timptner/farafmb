from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Program, Mentor, Helper


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
