from django import forms
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError


class ImageForm(forms.Form):
    file = forms.ImageField(
        label="Gruppenfoto",
        widget=forms.FileInput(attrs={'class': "file-input"}),
    )

    def clean_file(self):
        data = self.cleaned_data['file']
        if data.name.endswith('.jpg'):
            data.name = data.name.rstrip('.jpg') + '.jpeg'
        if not data.name.endswith('.jpeg'):
            raise ValidationError("Es sind nur Bilder des Datei-Typs JPG erlaubt.")
        data.name = 'team.jpeg'
        return data

    def save(self):
        file = self.cleaned_data['file']
        path = 'about/' + file.name
        if default_storage.exists(path):
            default_storage.delete(path)
        default_storage.save(path, file)
