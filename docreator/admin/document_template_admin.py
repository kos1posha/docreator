from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from docreator.models import DocumentTemplate


class DocumentTemplateAdmin(ModelAdmin):
    fieldsets = [
        [None, {'fields': ['user', 'content', 'name', 'description']}],
        ['Свойства', {'fields': ['jinja_fields', 'instances']}]
    ]
    add_fieldsets = [
        [None, {'fields': ['user', 'content', 'name', 'description']}],
    ]

    list_display = ['safe_name', 'user_link', 'content']
    list_filter = ['user']
    search_fields = ['user']
    readonly_fields = ['user', 'content', 'jinja_fields', 'instances']
    ordering = ['user', '-id']

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets if obj else self.add_fieldsets

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []

    @admin.display(description='Название')
    def safe_name(self, obj: DocumentTemplate):
        return obj.safe_name

    @admin.display(description='Пользователь')
    def user_link(self, obj: DocumentTemplate):
        user_href = reverse('admin:users_user_change', args=[obj.user.id])
        return mark_safe(f'<div class="readonly"><a href="{user_href}">{obj.user.username}</a></div>')

    @admin.display(description='Поля')
    def jinja_fields(self, obj: DocumentTemplate):
        html = []
        for field in sorted(obj.fields, key=(lambda f: f.name_in_template)):
            field_href = reverse('admin:docreator_field_change', args=[field.id])
            html.append(f'<div class="readonly"><a href="{field_href}">{field.name_in_template}</a></div>')
        return mark_safe(''.join(html)) if html else 'Отсутствуют'

    @admin.display(description='Экземпляры')
    def instances(self, obj: DocumentTemplate):
        html = []
        for instance in obj.instances:
            instance_href = reverse('admin:docreator_documentinstance_change', args=[instance.id])
            html.append(f'<div class="readonly"><a href="{instance_href}">{instance.safe_name}</a></div>')
        return mark_safe(''.join(html)) if html else 'Отсутствуют'
