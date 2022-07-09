from django.contrib import admin

from .models import Program, Mentor


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['faculty']


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_filter = ['program__faculty']
