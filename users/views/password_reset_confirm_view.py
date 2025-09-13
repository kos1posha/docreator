from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from users.forms.password_reset_confirm_form import PasswordResetConfirmForm


class PasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('docreator:index')
    success_message = 'Пароль успешно изменен'
    extra_context = {
        'title': 'Установить новый пароль',
        'submit': 'Установить',
    }
