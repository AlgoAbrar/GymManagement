from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailVerifiedBackend(ModelBackend):
    """
    Authenticate only if user.is_active and user.is_verified is True.
    Accepts username or email in the 'username' argument.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and user.is_active and getattr(user, "is_verified", False):
            return user
        return None
