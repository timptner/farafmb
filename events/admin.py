from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from .forms import EventForm
from .models import Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'comment', 'is_approved', 'registered_at')
    list_filter = ('event__title',)
    ordering = ['registered_at']
    actions = [
        'make_approved',
        'make_rejected',
    ]

    @admin.action(description=_("Mark selected participants as approved"))
    def make_approved(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, ngettext_lazy(
            "%d participants was successfully marked as approved.",
            "%d participants were successfully marked as approved.",
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description=_("Mark selected participants as rejected"))
    def make_rejected(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, ngettext_lazy(
            "%d participants was successfully marked as rejected.",
            "%d participants were successfully marked as rejected.",
            updated,
        ) % updated, messages.SUCCESS)
