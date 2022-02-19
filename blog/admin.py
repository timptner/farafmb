import re

from django.contrib import admin, messages

from .models import Snippet, Post, Image, Video, Link


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


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'visible')
