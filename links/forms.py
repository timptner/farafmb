from django import forms
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
