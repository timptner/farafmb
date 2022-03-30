from django.contrib import admin

from .models import Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ('event__title',)
