from django.contrib.auth.forms import SetPasswordForm

from .sign_in_form import SingInForm
from .sign_up_form import SingUpForm


class UserSetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
