from django.contrib import admin

from .forms import JobForm, DocumentForm
from .models import Job, Document


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = ('title', 'is_expired', 'created_on')
    date_hierarchy = 'created_on'
    search_fields = ['title', 'content']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
