from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_expired', 'created_on')
    date_hierarchy = 'created_on'
    search_fields = ['title', 'content']
