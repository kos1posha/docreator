from django.contrib.auth.password_validation import get_default_password_validators


def get_password_validators():
    return [
        validator.validate
        for validator
        in get_default_password_validators()
    ]