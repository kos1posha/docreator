from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, EmailInput, TextInput

from users.models import User

UserModel: User = get_user_model()


class SingUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

    username = CharField(
        label='Имя пользователя',
        help_text='Только латинские буквы, цифры и нижнее подчёркивание',
        error_messages={
            'required': 'Обязательное поле',
        },
        widget=TextInput(
            attrs={
                'autocapitalize': 'none',
                'maxlength': '30',
            },
        ),
    )
    email = CharField(
        label='Адрес электронной почты',
        help_text='Не используется для рекламы и рассылок',
        max_length=254,
        error_messages={
            'required': 'Обязательное поле',
            'invalid': 'Недопустимый адрес электронной почты',
        },
        widget=EmailInput(
            attrs={
                'autocomplete': 'email',
            },
        ),
    )
    password1 = CharField(
        label='Пароль',
        help_text='Содержит не менее 8 символов',
        strip=False,
        error_messages={
            'required': 'Обязательное поле',
        },
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            },
        ),
    )
    password2 = CharField(
        label='Подтвердите пароль',
        help_text='Для подтверждения введите пароль ещё раз',
        strip=False,
        error_messages={
            'required': 'Обязательное поле',
        },
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            },
        ),
    )

    error_messages = {
        'password_too_short': 'Пароль слишком короткий',
        'password_mismatch': 'Пароли не совпадают',
    }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1)
        except ValidationError:
            exc_code = 'password_too_short'
            raise ValidationError(
                self.error_messages[exc_code],
                code=exc_code
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            exc_code = 'password_mismatch'
            raise ValidationError(
                self.error_messages[exc_code],
                code=exc_code
            )
        return password2
