from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Link


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url', 'text', 'icon', 'position', 'is_active')
        help_texts = {
            'icon': _("You can use any free or sponsored icon from FontAwesome "
                      "v5. Please consider reading the documentation of "
                      "FontAwesome on how to use icons."),
            'position': _("The higher the value, the further below it will "
                          "be listed. Every position must be unique across all "
                          "existing links."),
            'is_active': _("Specify if this link is visible or not."),
        }


class ChangeOrderForm(forms.Form):
    order = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean_order(self):
        data = self.cleaned_data['order']
        positions = data.split(',')
        if any([not position.isdigit() for position in positions]):
            raise ValidationError(_("Not all positions are integers."))
        data = [int(position) for position in positions]
        return data

    def save(self):
        order = self.cleaned_data.get('order')
        links = []
        for position in order:
            link = Link.objects.get(pk=position)
            link.position = order.index(position)
            links.append(link)
        Link.objects.update(position=None)
        Link.objects.bulk_update(links, ['position'])
