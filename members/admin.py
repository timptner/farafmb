import secrets
import time

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy

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

    @admin.action(description="Send selected users a new strong password")
    def send_password_reset_mail(self, request, queryset):
        for user in queryset:
            password = secrets.token_urlsafe(16)
            user.password = make_password(password)
            user.save()
            send_mail(
                "Dein Passwort wurde zurückgesetzt",
                f"""Hallo {user.first_name},
    
    dein Passwort wurde durch einen Administrator zurückgesetzt. Im Folgenden findest du deine neues Passwort.
    
    Benutzername:   {user.username}
    Passwort:       {password}
    
    Bitte ändere dein Passwort zeitnah unter: {request.scheme}://{request.get_host()}{reverse_lazy('admin:password_change')}
    
    Viele Grüße
    FaRaFMB""",
                None,
                [user.email],
            )
            self.message_user(request,
                              "Successfully changed password for '%s' and "
                              "send new password via email to this user." % user,
                              messages.SUCCESS)
            time.sleep(10)  # TODO Use cleaner way to throttle email sending


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
