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
        )
        return user

    def update_user(self, user, claims):
        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

