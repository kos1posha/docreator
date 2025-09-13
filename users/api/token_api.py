from django.contrib.auth import authenticate
from knox.auth import TokenAuthentication
from knox.views import LoginView, LogoutView, LogoutAllView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class LoginTokenView(LoginView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        if request.user.is_authenticated:
            return super().post(request, format)
        errors = {}
        username, password = request.data.get('username', ''), request.data.get('password', '')
        if not username:
            errors['username'] = ['Обязательное поле']
        if not password:
            errors['password'] = ['Обязательное поле']
        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        if not (user := authenticate(username=username, password=password)):
            return Response(data={'non_field': ['Неверные логин и пароль']}, status=status.HTTP_401_UNAUTHORIZED)
        request.user = user
        return super().post(request, format)


class LogoutTokenView(LogoutView):
    http_method_names = ['post']
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        return super().post(request, format)


class LogoutAllTokensView(LogoutAllView):
    http_method_names = ['post']
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        return super().post(request, format)
