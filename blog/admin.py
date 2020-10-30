import re

from django.contrib import admin, messages

from .models import Snippet, Post, Image


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if re.search(r'!\[.+]\(.+\)', obj.content):
            messages.warning(request, "Einbetten von Bildern per Hyperlink wird blockiert. "
                                      "Bitte 'Blog->Images' verwenden.")

        super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if re.search(r'!\[.+]\(.+\)', obj.content):
            messages.warning(request, "Einbetten von Bildern per Hyperlink wird blockiert. "
                                      "Bitte 'Blog->Images' verwenden.")

        super().save_model(request, obj, form, change)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
