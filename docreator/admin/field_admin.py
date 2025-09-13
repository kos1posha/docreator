from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from docreator.models import Field


class FieldAdmin(ModelAdmin):
    fieldsets = [
        [None, {'fields': ['template_link', 'name_in_template', 'type', 'label', 'help_text', 'default', 'min', 'max']}]
    ]

    list_display = ['name_in_template', 'template_link', 'type_link']
    list_filter = ['template', 'type']
    readonly_fields = ['template_link', 'name_in_template']
    search_fields = ['template', 'name_in_template', 'type', 'label']
    ordering = ['template', 'name_in_template']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(description='Шаблон')
    def template_link(self, obj: Field):
        template_href = reverse('admin:docreator_documenttemplate_change', args=[obj.template.id])
        return mark_safe(f'<div class="readonly"><a href="{template_href}">{obj.template.safe_name}</a></div>')

    @admin.display(description='Тип')
    def type_link(self, obj: Field):
        type_href = reverse('admin:docreator_fieldtype_change', args=[obj.type.id])
        return mark_safe(f'<div class="readonly"><a href="{type_href}">{obj.type.code}</a></div>')
