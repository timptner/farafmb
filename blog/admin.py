from django.contrib import admin

from .models import Snippet, Post, Image


admin.site.register(Snippet)
admin.site.register(Post)
admin.site.register(Image)
