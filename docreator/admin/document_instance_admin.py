from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from docreator.models import DocumentInstance


class DocumentInstanceAdmin(ModelAdmin):
    fieldsets = [
        [None, {'fields': ['user_link', 'template_link', 'name']}],
        ['Отслеживаемые даты', {'fields': ['created', 'modified']}],
        ['Свойства', {'fields': ['values']}],
    ]
    add_fieldsets = [
        [None, {'fields': ['template', 'name']}],
    ]

    list_display = ['safe_name', 'template_link', 'user_link', 'created', 'modified']
    list_filter = ['template']
    readonly_fields = ['template_link', 'user_link', 'values', 'created', 'modified']
    search_fields = ['user_link', 'name']

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets if obj else self.add_fieldsets

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []

    @admin.display(description='Название')
    def safe_name(self, obj: DocumentInstance):
        return obj.safe_name

    @admin.display(description='Пользователь')
    def user_link(self, obj: DocumentInstance):
        user_href = reverse('admin:users_user_change', args=[obj.user.id])
        return mark_safe(f'<div class="readonly"><a href="{user_href}">{obj.user.username}</a></div>')

    @admin.display(description='Шаблон')
    def template_link(self, obj: DocumentInstance):
        template_href = reverse('admin:docreator_documenttemplate_change', args=[obj.template.id])
        return mark_safe(f'<div class="readonly"><a href="{template_href}">{obj.template.safe_name}</a></div>')

    @admin.display(description='Значения')
    def values(self, obj: DocumentInstance):
        html = []
        for value in obj.values:
            value_href = reverse('admin:docreator_value_change', args=[value.id])
            html.append(f'<div class="readonly"><a href="{value_href}">{value.name_in_template} = {value.value}</a></div>')
        return mark_safe(''.join(html)) if html else 'Отсутствуют'
