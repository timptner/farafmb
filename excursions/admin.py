from django.contrib import admin

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
