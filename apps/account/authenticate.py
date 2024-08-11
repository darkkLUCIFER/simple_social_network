from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailBackend(BaseBackend):
    """
    custom authentication backend that allows users to log in using their email address
    """

    # The `authenticate` method is called to validate a user based on the provided credentials.

    def authenticate(self, request, username=None, password=None):
        try:
            # Attempt to retrieve a user based on the provided email address (stored in `username`)
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    # The `get_user` method is used to retrieve a user object based on their user ID
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
