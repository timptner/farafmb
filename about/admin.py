from django.contrib import admin
from django.contrib.flatpages import admin as flatpages_admin
from django.contrib.flatpages.models import FlatPage


class FlatpageForm(flatpages_admin.FlatpageForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["content"].help_text = (
            'Verwende <a target="blank" href="https://www.markdownguide.org/cheat-sheet/">Markdown</a> zur '
            'Formatierung.'
        )


class FlatPageAdmin(flatpages_admin.FlatPageAdmin):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
