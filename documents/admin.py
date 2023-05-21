from django.contrib import admin

from .forms import DocumentAdminForm
from .models import Document, Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'visible')
    list_filter = ('group', 'visible')
    date_hierarchy = 'created'
    form = DocumentAdminForm
