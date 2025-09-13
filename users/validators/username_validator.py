from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^(?=^.{2,30}$)[a-z0-9_]+$',
    flags=2,
    code='invalid',
    message='Недопустимое имя пользователя',
)

username_length_validator = RegexValidator(
    regex=r'(?=^.{2,30}$)',
    code='invalid_length',
    message='Допустимая длина от 2 до 30 символов',
)

username_symbol_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    code='invalid_symbols',
    message='Присутствуют недопустимые символы',
)


def get_username_validator():
    return [
        username_validator
    ]


def get_username_detail_validators():
    return [
        username_length_validator,
        username_symbol_validator,
    ]
