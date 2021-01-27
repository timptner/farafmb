from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Group


class KeycloakBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        is_member = '/Member/Fachschaftsrat Maschinenbau' in claims.get('groups', [])
        return verified and is_member

    def create_user(self, claims):
        user = super().create_user(claims)

        roles = claims.get('roles', [])
        groups = Group.objects.filter(name__in=roles)

        user.username = claims.get('preferred_username', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email', '')
        user.is_staff = True
        user.is_superuser = 'admin' in roles
        user.groups.add(*groups)
        user.save()

        return user

    def update_user(self, user, claims):
        roles = claims.get('roles', [])
        groups = Group.objects.filter(name__in=roles)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.is_superuser = 'admin' in roles
        if groups.count() == 0:
            user.groups.clear()
        elif user.groups.count() == 0:
            user.groups.add(*groups)
        else:
            new_groups = set(groups.values_list('id', flat=True).get())
            old_groups = set(user.groups.values_list('id', flat=True).get())
            if new_groups != old_groups:
                user.groups.clear()
                user.groups.add(*groups)
        user.save()

        return user
