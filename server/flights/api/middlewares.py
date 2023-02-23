from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class CustomTokenAuthentication(TokenAuthentication):
    """
    Personalized middleware for token authentication.
    """
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('The user associated with this token is inactive')

        return (token.user, token)

    def get_user_from_token(self, token_key):
        print('entre al get_user_from_token')
        try:
            token = self.model.objects.get(key=token_key)
        except self.model.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return token.user
