from django import forms
from django.core.validators import RegexValidator


class UpdateForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "input"
            },
        ),
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_/\s]+$',
                "Es sind nur die alphanumerische Zeichen sowie Binde-, Unter-, und Schrägstrich erlaubt.",
                'disallowed-symbols',
            ),
            RegexValidator(
                r'^[a-zA-Z0-9].+[a-zA-Z0-9]$',
                "Der Titel muss muss mit alphanumerischen Zeichen beginnen und enden.",
                'disallowed-start-or-end',
            )
        ]
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': "textarea",
                'rows': 15,
                'style': "font-family: monospace;",
            },
        ),
    )

    def clean_title(self):
        data = self.cleaned_data['title']
        data.replace(' ', '_')
        return data
