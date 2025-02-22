from django.contrib import admin
from members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "joined_at"]
    list_filter = ["department", "course"]
    ordering = ["name", "email"]
