from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import OfficeHour


@admin.register(OfficeHour)
class OfficeHourAdmin(admin.ModelAdmin):

    actions = ['make_visible', 'make_invisible']

    @admin.action(description='Mark selected office hours as visible')
    def make_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        self.message_user(request, ngettext(
            '%d office hours was successfully marked as visible.',
            '%d office hours were successfully marked as visible.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected office hours as invisible')
    def make_invisible(self, request, queryset):
        updated = queryset.update(is_visible=False)
        self.message_user(request, ngettext(
            '%d office hours was successfully marked as invisible.',
            '%d office hours were successfully marked as invisible.',
            updated,
        ) % updated, messages.SUCCESS)
