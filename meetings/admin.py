from django.contrib import admin

from meetings.models import Meeting, Template


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass
