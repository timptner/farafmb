from django.contrib import admin

from .models import Excursion, Participant


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'seats', 'visit_on')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_car_owner')
    list_filter = ('excursion__title', 'is_car_owner')
