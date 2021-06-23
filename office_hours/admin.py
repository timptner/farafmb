from django.contrib import admin

from .models import OfficeHour


@admin.register(OfficeHour)
class OfficeHourAdmin(admin.ModelAdmin):
    pass
