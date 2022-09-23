from django import forms as _forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from farafmb import forms

from .models import Order


class OrderForm(forms.ModelForm):
    sizes = _forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_("Shoe sizes"),
        help_text=_("You can order multiple sizes by separating them with commas. If you "
                    "specify a size multiple times, it will be ordered accordingly often."),
        required=True
    )
    confirmation = _forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'data-text': _("I hereby confirm that my order is binding.")}),
        label=_("Consent"),
        required=True
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']

    def clean_sizes(self):
        data = self.cleaned_data['sizes']

        try:
            data = [int(item.strip()) for item in data.split(',')]
        except ValueError:
            raise ValidationError(_("Only numbers are allowed."), code='invalid')

        if min(data) < 30:
            raise ValidationError(_("Minimum shoe size is 30."))

        if max(data) >= 50:
            raise ValidationError(_("Maximum shoe size is 49."))

        return data
