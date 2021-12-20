from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    actions = ['remove_password']

    @admin.action(description="Set unusable password for selected users")
    def remove_password(self, request, queryset):
        for user in queryset:
            user.set_unusable_password()
            user.save()
        self.message_user(request,
                          "Successfully set unusable passwords for '%s' users." % len(queryset),
                          messages.SUCCESS)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
