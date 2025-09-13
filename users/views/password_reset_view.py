from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from users.forms.password_reset_form import PasswordResetForm


class PasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'generic_form.html'
    email_template_name = 'users/password_reset_mail.html'
    success_url = reverse_lazy('docreator:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля было отправлено на вашу почту'
    extra_context = {
        'title': 'Восстановление пароля',
        'submit': 'Отправить',
        'description': 'Введите адрес электронной почты, к которой привязан ваш аккаунт, чтобы '
                       'мы могли отправить вам инструкцию по восстановлению пароля',
    }
