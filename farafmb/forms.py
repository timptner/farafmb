from django.forms.renderers import TemplatesSetting
from django.forms import fields, ModelForm as _ModelForm


class BulmaFormRenderer(TemplatesSetting):
    form_template_name = 'forms/layout.html'
    # formset_template_name = 'django/forms/formsets/default.html'


class ModelForm(_ModelForm):
    template_name_label = 'forms/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class TextInput(fields.TextInput):
    template_name = 'forms/widgets/input.html'


class NumberInput(fields.NumberInput):
    template_name = 'forms/widgets/input.html'


class EmailInput(fields.EmailInput):
    template_name = 'forms/widgets/input.html'


class Textarea(fields.Textarea):
    template_name = 'forms/widgets/textarea.html'


class CheckboxInput(fields.CheckboxInput):
    template_name = 'forms/widgets/checkbox.html'
