from rest_framework.routers import DefaultRouter

from .token_api import LoginTokenView, LogoutAllTokensView, LogoutTokenView
from .user_api import UserPermission, UserSerializer, UserViewSet

class ApiRouter(DefaultRouter):
    root_view_name = 'root'
