from anonymous_auth.models import User


class IsAnonymousUserWithCredentials:
    def has_permission(self, request, view):
        return bool(request.auth and isinstance(request.auth, User))
