from django.contrib import admin
from members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "joined_at", "is_visible"]
    list_filter = ["department", "program", "is_visible"]
    ordering = ["name", "email"]
