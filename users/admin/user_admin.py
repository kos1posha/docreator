from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import User


class UserAdmin(UserAdmin):
    fieldsets = [
        ['Аккаунт', {'fields': ['username', 'password']}],
        ['Персональная информация', {'fields': ['email', 'avatar', 'avatar_preview']}],
        ['Статусы', {'fields': ['is_active', 'is_superuser']}],
        ['Отслеживаемые даты', {'fields': ['last_login', 'date_joined']}],
    ]
    add_fieldsets = [
        ('Обязательные поля', {
            'classes': ['wide'],
            'fields': ['username', 'email', 'password1', 'password2']
        })
    ]

    list_display = ['username', 'email', 'is_active', 'is_superuser']
    list_filter = ['is_active', 'is_superuser']
    readonly_fields = ['last_login', 'date_joined', 'avatar_preview']
    search_fields = ['username', 'email']
    ordering = ['-is_superuser', 'username']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ['email'] if obj else self.readonly_fields

    @admin.display(description='Предпросмотр')
    def avatar_preview(self, obj: User):
        if not obj.avatar:
            return '-'
        return mark_safe(f'<img src="{obj.avatar.url}" width="300" alt="Нет фото">')
