from django.contrib import admin

from .forms import EventForm
from .models import Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ('event__title',)
