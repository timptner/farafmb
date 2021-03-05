from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import validate_email
from meetings.models import Template

User = get_user_model()


class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)


class InviteForm(forms.Form):
    members = MultiEmailField(label="Mitglieder", initial=', '.join(User.objects.values_list('email', flat=True)),
                              widget=forms.TextInput(attrs={'class': "input"}))
    guests = MultiEmailField(label="Gäste", widget=forms.TextInput(attrs={'class': "input"}), required=False)
    subject = forms.CharField(label="Betreff", initial="Einladung zur Sitzung",
                              widget=forms.TextInput(attrs={'class': "input"}), required=True)
    message = forms.CharField(label="Nachricht", widget=forms.Textarea(attrs={'class': "textarea"}), required=True)

    def __init__(self, *args, **kwargs):
        meeting = kwargs.pop('meeting')
        template = Template.objects.get(slug='invitation')
        super().__init__(*args, **kwargs)
        self.fields['guests'].initial = ', '.join(meeting.guests.split(','))
        self.fields['message'].initial = template.content.format(date=meeting.date.strftime('%d.%m.%Y'), agenda=meeting.agenda)

    def send_mail(self):
        send_mail(
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
            None,
            self.cleaned_data['members'] + self.cleaned_data['guests'],
        )
