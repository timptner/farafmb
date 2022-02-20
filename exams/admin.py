from django.contrib import admin, messages
from django.utils.translation import ngettext_lazy, gettext_lazy as _

from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    readonly_fields = ('minute_file', 'minute_author', 'submitted_on')
    list_display = ('course', 'date', 'is_archived')
    list_filter = ('minute_author', 'submitted_on', 'is_archived')
    actions = ['remove_minute_author', 'mark_as_archived']

    def remove_minute_author(self, request, queryset):
        updated = queryset.update(minute_author=None)
        error_message = ngettext_lazy(
            "%d author was removed successfully.",
            "%d authors were removed successfully.",
        )
        self.message_user(request, error_message % updated, messages.SUCCESS)
    remove_minute_author.short_description = _("Make selected exams anonymous")

    def mark_as_archived(self, request, queryset):
        updated = queryset.update(is_archived=True)
        error_message = ngettext_lazy(
            "%d exam was marked as archived.",
            "%d exams were marked as archived.",
        )
        self.message_user(request, error_message % updated, messages.SUCCESS)
    mark_as_archived.short_description = _("Archive selected exams")
