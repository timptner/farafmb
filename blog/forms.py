from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from farafmb import forms

from .models import Post


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(),
        }
        help_texts = {
            'content': _("You can use Markdown to format the text."),
        }

