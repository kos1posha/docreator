from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from docreator.models import Value


class ValueAdmin(ModelAdmin):
    fieldsets = [
        [None, {'fields': ['value', 'instance_link', 'field_link']}]
    ]

    list_display = ['value', 'field_link', 'instance_link']
    list_filter = ['instance']
    readonly_fields = ['field_link', 'instance_link']
    search_fields = ['instance', 'name_in_template']
    ordering = ['instance', 'field']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(description='Поле')
    def field_link(self, obj: Value):
        field_href = reverse('admin:docreator_field_change', args=[obj.field.id])
        return mark_safe(f'<div class="readonly"><a href="{field_href}">{obj.field.name_in_template}</a></div>')

    @admin.display(description='Экземпляр')
    def instance_link(self, obj: Value):
        instance_href = reverse('admin:docreator_documentinstance_change', args=[obj.instance.id])
        return mark_safe(f'<div class="readonly"><a href="{instance_href}">{obj.instance.full_name}</a></div>')