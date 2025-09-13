from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import SingInForm


class SignInView(SuccessMessageMixin, LoginView):
    authentication_form = SingInForm
    template_name = 'users/sign_form.html'
    success_message = 'Добро пожаловать на сайт'
    extra_context = {
        'title': 'Вход',
        'sign': 'in',
    }

    def get_success_message(self, cleaned_data):
        return f'{self.success_message}, {self.request.user.username}!' % cleaned_data
