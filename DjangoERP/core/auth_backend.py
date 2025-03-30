from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class GuestBackend(BaseBackend):
    """
    Authenticate as a guest user for anonymous sessions
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username == 'guest' and password == 'guest':
            try:
                user = User.objects.get(username='guest')
                return user
            except User.DoesNotExist:
                # Create a guest user if it doesn't exist
                user = User(username='guest', email='guest@example.com', is_staff=False, is_superuser=False)
                user.set_unusable_password()  # Can't login normally with this user
                user.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
