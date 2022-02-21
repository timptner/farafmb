from django.contrib import admin

from .forms import LinkAdminForm
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'position', 'is_active')
    list_filter = ('is_active',)
    form = LinkAdminForm
