from django.urls import path

from users.api import LoginTokenView, LogoutAllTokensView, LogoutTokenView


urlpatterns = [
    path('login/', LoginTokenView.as_view(), name='token-in'),
    path('logout/', LogoutTokenView.as_view(), name='token-out'),
    path('logout/all/', LogoutAllTokensView.as_view(), name='token-out-all'),
]