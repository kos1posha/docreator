from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = CharField(
        label='Новый пароль',
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
    new_password2 = CharField(
        label='Подтверждение нового пароля',
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
        try: validate_password(password1)
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
