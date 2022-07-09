from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Mentor


class MentorForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True, label=_("Privacy"))

    class Meta:
        model = Mentor
        fields = ['first_name', 'last_name', 'email', 'phone', 'program']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
        }
