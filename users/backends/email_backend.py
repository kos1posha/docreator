from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


UserModel: User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist: return None
        else: return user if user.check_password(password) else None

    def get_user(self, user_id):
        try: user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist: return None
        else: return user
