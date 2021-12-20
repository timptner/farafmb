from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        username = claims.get('preferred_username')
        if not username:
            return self.UserModel.objects.none()

        try:
            user = self.UserModel.objects.get(username=username)
            return [user]

        except self.UserModel.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        user = self.UserModel.objects.create_user(
            username=claims.get('preferred_username'),
            email=claims.get('email'),
            first_name=claims.get('given_name'),
            last_name=claims.get('family_name'),
            is_staff=True,
        )

        # Check if superuser
        if 'admin' in claims.get('roles', []):
            user.is_admin = True

        # Add user permissions via groups
        self._add_groups(user, claims)

        user.save()

        return user

    def update_user(self, user, claims):
        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        # Check if superuser
        if 'admin' in claims.get('roles', []):
            user.is_admin = True
        else:
            user.is_admin = False

        # Remove user permissions via groups
        for group in user.groups.all():
            if group.name not in claims.get('roles', []):
                user.groups.remove(group)

        # Add user permissions via groups
        self._add_groups(user, claims)

        user.save()

        return user

    @staticmethod
    def _add_groups(user, claims):
        for role in claims.get('roles', []):
            if role == 'admin':
                continue
            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                group = Group.objects.create(name=role)

            user.groups.add(group)

