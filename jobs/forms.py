from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('slug'):
            self.fields['slug'].disabled = True
            self.fields['slug'].help_text = "Dieses Feld kann nicht verändert werden. " \
                                            "Bitte wende dich ggf. an den Administrator."
        else:
            self.fields['slug'].help_text = "Dieses Feld kann nachträglich nicht mehr verändert werden."

    class Meta:
        model = Job
        fields = ('title', 'slug', 'desc', 'file', 'expired_on')
