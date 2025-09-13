from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.safestring import mark_safe

from users.models import AuthToken


class AuthTokenAdmin(ModelAdmin):
    fieldsets = [
        ['Спецификация', {'fields': ['token', 'key']}],
        ['Принадлежит', {'fields': ['user_link']}],
        ['Даты', {'fields': ['expired_datetime', 'created_datetime']}],
    ]

    list_display = ['token', 'user_link', 'expired_date']
    readonly_fields = ['token', 'key', 'user_link', 'expired_datetime', 'created_datetime']
    search_fields = ['user']
    ordering = ['created']

    @admin.display(description='Токен')
    def token(self, obj: AuthToken):
        return f'****{obj.digest[40:-40]}****'

    @admin.display(description='Ключ')
    def key(self, obj: AuthToken):
        return obj.token_key

    @admin.display(description='Пользователь', ordering='')
    def user_link(self, obj: AuthToken):
        user_href = reverse('admin:users_user_change', args=[obj.user_id])
        return mark_safe(f'<div class="readonly"><a href="{user_href}">admin</a></div>')

    @admin.display(description='Истечет')
    def expired_date(self, obj: AuthToken):
        return date_format(obj.expiry.date())

    @admin.display(description='Истечет')
    def expired_datetime(self, obj: AuthToken):
        return date_format(obj.expiry)

    @admin.display(description='Создан')
    def created_datetime(self, obj: AuthToken):
        return date_format(obj.created)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
