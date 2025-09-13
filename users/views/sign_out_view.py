from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin


class SignOutView(SuccessMessageMixin, LogoutView):
    success_message = 'Вы вышли из профиля'

    def get_success_message(self, cleaned_data):
        return f'{self.success_message} {self.request.user.username}' % cleaned_data
