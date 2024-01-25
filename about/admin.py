from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Image.objects.count() > 0:
            return False
        return super().has_add_permission(request)
