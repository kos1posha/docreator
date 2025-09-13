from knox.models import AuthToken as KnoxAuthToken


class AuthToken(KnoxAuthToken):
    class Meta:
        proxy = True
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    def __str__(self):
        return f'Токен пользователя {self.user}'
