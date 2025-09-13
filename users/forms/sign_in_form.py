from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, TextInput


class SingInForm(AuthenticationForm):
    username = CharField(
        label='Имя пользователя или почтовый адрес',
        required=False,
        widget=TextInput(
            attrs={
                'autofocus': True,
                'autocapitalize': 'none',
                'autocomplete': 'email',
            },
        ),
    )
    password = CharField(
        label='Пароль',
        required=False,
        strip=False,
        widget=PasswordInput(
            attrs={
                'autocomplete': 'current-password',
            },
        ),
    )

    error_messages = {
        'invalid_login': 'Неверные логин и пароль',
        'inactive': 'Данный пользователь неактивен',
        'empty': 'Введите данные, чтобы продолжить',
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password:
            exc_code = 'empty'
            raise ValidationError(
                self.error_messages[exc_code],
                code=exc_code
            )
        super().clean()
