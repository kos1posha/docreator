from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, EmailField, ImageField
from django.utils import timezone
import unicodedata

from docreator.models import DocumentInstance, DocumentTemplate
from users.validators import get_username_detail_validators


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username: raise ValueError('The given username must be set')
        if not email: raise ValueError('The given email must be set')
        username = self.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try: email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError: pass
        else: email = email_name + '@' + domain_part.lower()
        return email


def user_avatar_storage(user, filename):
    format = filename.split('.')[-1]
    return f'avatars/{user.username}.{timezone.now().date()}.{format}'


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    username = CharField(
        verbose_name='Имя пользователя',
        max_length=30,
        unique=True,
        error_messages={'unique': 'Данное имя пользователя уже используется', 'max_length': ''},
        validators=get_username_detail_validators(),
    )
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        error_messages={'unique': 'Данный адрес электронной почты уже используется', 'max_length': 'Длина почтового ящика не может превышать 254 символа'},
    )
    password = CharField(
        verbose_name='Пароль',
        max_length=128,
    )
    avatar = ImageField(
        verbose_name='Фото профиля',
        upload_to=user_avatar_storage,
        blank=True,
        null=True,
    )
    last_login = DateTimeField(
        verbose_name='Последний вход',
        blank=True,
        null=True,
    )
    date_joined = DateTimeField(
        verbose_name='Зарегистрирован',
        default=timezone.now,
    )
    is_active = BooleanField(
        verbose_name='Активен',
        default=True,
    )
    is_staff = BooleanField(
        verbose_name='Статус персонала',
        default=False,
    )
    is_superuser = BooleanField(
        verbose_name='Статус суперпользователя',
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def document_templates(self):
        return DocumentTemplate.objects.filter(user=self)

    @property
    def document_instances(self):
        return DocumentInstance.objects.filter(template__user=self)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
