from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SingUpForm
from users.models import User


UserModel: User = get_user_model()


class SignUpView(SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = SingUpForm
    template_name = 'users/sign_form.html'
    success_url = reverse_lazy('users:sign-in')
    success_message = 'Регистрация прошла успешно'
    extra_context = {
        'title': 'Регистрация',
        'sign': 'up',
    }
