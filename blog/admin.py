import re

from calendar import monthrange
from datetime import date
from django.contrib import admin, messages
from django.utils.translation import ngettext
from typing import Tuple

from .models import Snippet, Post, Image, Video, Protocol, Link


def check_img(request, content: str):
    if re.search(r'!\[.+]\(.+\)', content):
        messages.warning(request, "Einbetten von Bildern per Hyperlink wird blockiert. "
                                  "Bitte 'Blog->Images' verwenden.")


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('desc', 'slug', 'created')

    def save_model(self, request, obj, form, change):
        check_img(request, obj.content)
        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('author',)
    list_display = ('title', 'image', 'video', 'author', 'created')
    list_filter = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        check_img(request, obj.content)
        super().save_model(request, obj, form, change)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created')


def calculate_semester(date_: date) -> Tuple[date, str]:
    """Return first day of semester"""
    year = date_.year
    month = date_.month
    if month < 4:
        # WS of last year
        return date(year - 1, 10, 1), f"{year - 1} WiSe"
    elif month < 10:
        # SS of current year
        return date(year, 4, 1), f"{year} SoSe"
    else:
        # WS of current year
        return date(year, 10, 1), f"{year} WiSe"


class SemesterListFilter(admin.SimpleListFilter):
    title = "Zeitraum"
    parameter_name = 'semester'

    def lookups(self, request, model_admin):
        dates = model_admin.model.objects.order_by('-date').values_list('date').distinct()
        return [calculate_semester(date_[0]) for date_ in dates]

    def queryset(self, request, queryset):
        if self.value():
            date_ = date.fromisoformat(self.value())
            year = date_.year
            month = (date_.month + 5) % 12
            if month == 3:
                year += 1
            day = monthrange(year, month)[1]
            return queryset.filter(date__gte=date_, date__lt=date(year, month, day))


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    readonly_fields = ('file', 'author', 'submitted')
    list_display = ('course', 'submitted')
    list_filter = (SemesterListFilter, 'author')
    actions = ['remove_author']

    def remove_author(self, request, queryset):
        updated = queryset.update(author=None)
        self.message_user(request, ngettext(
            '%d E-Mail-Adresse wurden erfolgreich entfernt.',
            '%d E-Mail-Adressen wurden erfolgreich entfernt.',
            updated,
        ) % updated, messages.SUCCESS)
    remove_author.short_description = "Ausgewählte Protokolle anonymisieren"


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'visible')
