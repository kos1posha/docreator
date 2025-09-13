from django.urls import path, re_path

from users.views import PasswordResetConfirmView, PasswordResetView, ProfileView, SignInView, SignOutView, SignUpView


app_name = 'users'
urlpatterns = [
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('sign/in/', SignInView.as_view(), name='sign-in'),
    path('sign/out/', SignOutView.as_view(), name='sign-out'),
    path('sign/up/', SignUpView.as_view(), name='sign-up'),
]
