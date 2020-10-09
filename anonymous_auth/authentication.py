from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
from anonymous_auth.models import User


class AnonymousAuthentication(TokenAuthentication):
    """
    Authenticates anonymous user and sets request.auth to custom User object
    if credentials of anonymous user are provided
    """
    keyword = 'Anonymous'
    model = User

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return AnonymousUser(), token
