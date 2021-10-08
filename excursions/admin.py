from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import ExcursionForm
from .models import Excursion, Participant


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    form = ExcursionForm
    list_display = ('__str__', 'seats', 'date')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_car_owner', 'is_seat_owner', 'created_on')
    list_filter = ('excursion__title', 'is_car_owner')
    ordering = ('created_on',)

    actions = ['contact_selected_participants']

    @admin.action(
        permissions=['add', 'change'],
        description="Send selected participants an email",
    )
    def contact_selected_participants(self, request, queryset):
        selected = queryset.order_by('pk').values_list('pk', flat=True)
        return HttpResponseRedirect(reverse_lazy('excursions:contact') + '?ids=%s' % (
            ','.join(str(pk) for pk in selected),
        ))
