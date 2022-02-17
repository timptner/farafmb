from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('member', 'day', 'time', 'is_visible')
    list_filter = ('is_visible', 'day')

    actions = ['make_visible', 'make_invisible']

    @admin.action(description='Mark selected consultation as visible')
    def make_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        self.message_user(request, ngettext(
            '%d consultation was successfully marked as visible.',
            '%d consultations were successfully marked as visible.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected consultations as invisible')
    def make_invisible(self, request, queryset):
        updated = queryset.update(is_visible=False)
        self.message_user(request, ngettext(
            '%d consultation was successfully marked as invisible.',
            '%d consultations were successfully marked as invisible.',
            updated,
        ) % updated, messages.SUCCESS)
