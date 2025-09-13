from django.contrib.auth.forms import PasswordResetForm
from django.forms import EmailInput, EmailField


class PasswordResetForm(PasswordResetForm):
    email = EmailField(
        label='Адрес электронной почты',
        max_length=254,
        error_messages={
            'required': 'Обязательное поле',

        },
        widget=EmailInput(
            attrs={
                'autofocus': True,
                'autocomplete': 'email',
            },
        ),
    )

    error_messages = {
        'invalid': 'Пользователь с таким адресом не найден',
    }
