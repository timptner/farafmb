from django.core.mail import EmailMessage
from django.core.validators import FileExtensionValidator
from django.forms import (Form, ValidationError,
                          EmailField, CharField, DateField, FileField, BooleanField,
                          EmailInput, TextInput, DateInput, FileInput)
from django.utils import timezone


class ProtocolForm(Form):
    email = EmailField(label="E-Mail-Adresse",
                       widget=EmailInput(attrs={'class': "input"}))

    course = CharField(label="Modul",
                       max_length=150,
                       widget=TextInput(attrs={'class': "input"}))

    lecturer = CharField(label="Dozent:in",
                         max_length=150,
                         widget=TextInput(attrs={'class': "input"}))

    date = DateField(label="Datum der Prüfung",
                     widget=DateInput(attrs={'type': 'date',
                                             'class': "input"}))

    file = FileField(label="Datei",
                     widget=FileInput(attrs={'class': "file-input"}),
                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    privacy = BooleanField(label="Datenschutz")

    def clean_email(self):
        data = self.cleaned_data['email']
        if data.split('@')[-1] != 'st.ovgu.de':
            raise ValidationError("Es kann nur die erlaubte Domain verwendet werden!", code='invalid')
        return data

    def clean_date(self):
        data = self.cleaned_data['date']
        if data > timezone.now().date():
            raise ValidationError("Das Datum darf nicht in der Zukunft liegen.", code='invalid_date')
        return data

    def clean_file(self):
        data = self.cleaned_data['file']
        if data.size > 2 * 10**6:
            size = str(round(data.size/10**6, 2)).replace('.', ',')
            raise ValidationError(f"Deine Datei ist mit {size} MB zu groß!",
                                  code='file_too_large')
        return data

    def send_email(self):
        file = self.cleaned_data['file']

        date = self.cleaned_data['date']
        semester = "SS" if date.month in range(4, 10) else "WS"
        if semester == "SS":
            semester += f" {date.year}"
        else:
            semester += f" {date.year}" if date.month > 9 else f" {date.year - 1}"

        email = self.cleaned_data['email']
        course = self.cleaned_data['course']
        lecturer = self.cleaned_data['lecturer']

        mail = EmailMessage(
            "Neues Protokoll",
            f"""Es wurde ein neues Protokoll von '{email}' eingereicht.

Modul: {course}
Dozent: {lecturer}
Datum: {date} ({semester})""",
            email,
            ['farafmb@ovgu.de'],
        )
        mail.attach(file.name, file.read(), file.content_type)
        mail.send()
