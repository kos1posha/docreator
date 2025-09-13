from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import BasePermission
from rest_framework.validators import UniqueValidator
from rest_framework.viewsets import ModelViewSet
from rest_framework.fields import ReadOnlyField, CharField, EmailField

from users.models import User
from users.validators import get_username_detail_validators


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    id = ReadOnlyField()
    username = CharField(
        label='Имя пользователя',
        validators=get_username_detail_validators() + [
            UniqueValidator(queryset=User.objects.all(), message='Данное имя пользователя уже используется')
        ],
        error_messages={
            'blank': 'Обязательное поле',
            'unique': 'Данное имя пользователя уже используется',
        },
        style={
            'autocapitalize': 'none',
            'maxlength': '30',
        },
    )
    email = EmailField(
        label='Адрес электронной почты',
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='Данный адрес электронной почты уже используется')
        ],
        error_messages={
            'blank': 'Обязательное поле',
            'unique': 'Данный адрес электронной почты уже используется',
            'invalid': 'Недопустимый адрес электронной почты',
        },
        style={
            'input_type': 'email',
            'autocomplete': 'email',
        },
    )
    password = CharField(
        label='Пароль',
        min_length=8,
        write_only=True,
        error_messages={
            'blank': 'Обязательное поле',
            'min_length': 'Пароль слишком короткий',
        },
        style={
            'input_type': 'password',
            'autocomplete': 'new-password',
        },
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        match view.action:
            case 'list':
                return request.user.is_authenticated and request.user.is_admin
            case 'create' | 'retrieve' | 'update' | 'partial_update' | 'destroy':
                return True
            case _:
                return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        match view.action:
            case 'retrieve':
                return obj == request.user or request.user.is_admin
            case 'update' | 'partial_update':
                return obj == request.user or request.user.is_admin
            case 'destroy':
                return request.user.is_admin
            case _:
                return False


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    http_method_names = ['get', 'post', 'patch', 'delete']
