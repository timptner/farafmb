from django.forms.renderers import TemplatesSetting
from django.forms import fields


class BulmaFormRenderer(TemplatesSetting):
    form_template_name = 'forms/layout.html'
    # formset_template_name = 'django/forms/formsets/default.html'


class TextInput(fields.TextInput):
    template_name = 'forms/widgets/input.html'


class Textarea(fields.Textarea):
    template_name = 'forms/widgets/textarea.html'
