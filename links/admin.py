from django.contrib import admin, messages
from django.utils.translation import ngettext_lazy, gettext_lazy as _

from .forms import LinkAdminForm
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'position', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('position',)
    form = LinkAdminForm
    actions = ['mark_as_active', 'mark_as_inactive']

    def get_changeform_initial_data(self, request):
        return {
            'icon': 'fas fa-link',
        }

    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        error_message = ngettext_lazy(
            "%d link was marked as active.",
            "%d links were marked as active.",
        )
        self.message_user(request, error_message % updated, messages.SUCCESS)
    mark_as_active.short_description = _("Set selected links active")

    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        error_message = ngettext_lazy(
            "%d link was marked as inactive.",
            "%d links were marked as inactive.",
        )
        self.message_user(request, error_message % updated, messages.SUCCESS)
    mark_as_inactive.short_description = _("Set selected links inactive")
