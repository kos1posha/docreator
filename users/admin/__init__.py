from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User, AuthToken
from .auth_token_admin import AuthTokenAdmin
from .user_admin import UserAdmin


admin.site.unregister(Group)

admin.site.register(AuthToken, AuthTokenAdmin)
admin.site.register(User, UserAdmin)
