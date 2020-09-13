from django.contrib import admin

from .models import Snippet, Post


admin.site.register(Snippet)
admin.site.register(Post)
