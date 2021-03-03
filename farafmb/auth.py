import logging

from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from typing import List

logger = logging.getLogger(__name__)


def get_valid_groups(roles: List[str]):
    """Return all available groups"""
    groups = Group.objects.filter(name__in=roles)
    group_names = [group.name for group in groups]
    roles_unknown = list(set(roles) - set(group_names))
    for role in roles_unknown:
        logger.warning(f"Ignoring role '{role}' because no matching group was found.")
    return groups


class KeycloakBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        is_member = '/Member/Fachschaftsrat Maschinenbau' in claims.get('groups', [])
        return verified and is_member

    def create_user(self, claims):
        user = super().create_user(claims)

        roles = claims.get('roles', [])
        superuser = 'admin' in roles
        if superuser:
            roles.remove('admin')

        # Create new user
        user.username = claims.get('preferred_username', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email', '')

        # Add user permissions
        user.is_superuser = superuser
        user.is_staff = True
        user.groups.add(*get_valid_groups(roles))

        user.save()
        return user

    def update_user(self, user, claims):
        roles = claims.get('roles', [])
        superuser = 'admin' in roles
        if superuser:
            roles.remove('admin')

        # Update user information
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        # Update user permissions
        user.is_superuser = superuser
        user.groups.clear()
        user.groups.add(*get_valid_groups(roles))

        user.save()
        return user
