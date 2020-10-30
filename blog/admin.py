import re

from django.contrib import admin, messages

from .models import Snippet, Post, Image


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('desc', 'slug', 'created')

    def save_model(self, request, obj, form, change):
        if re.search(r'!\[.+]\(.+\)', obj.content):
            messages.warning(request, "Einbetten von Bildern per Hyperlink wird blockiert. "
                                      "Bitte 'Blog->Images' verwenden.")

        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('author',)
    list_display = ('title', 'image', 'author', 'created')
    list_filter = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if re.search(r'!\[.+]\(.+\)', obj.content):
            messages.warning(request, "Einbetten von Bildern per Hyperlink wird blockiert. "
                                      "Bitte 'Blog->Images' verwenden.")

        super().save_model(request, obj, form, change)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created')
