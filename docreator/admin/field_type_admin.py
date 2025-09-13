from django.contrib.admin import ModelAdmin


class FieldTypeAdmin(ModelAdmin):
    fieldsets = [
        [None, {'fields': ['code', 'name', 'description']}],
    ]

    list_display = ['code', 'name']
    search_fields = ['code', 'name']
    readonly_fields = ['code']
    ordering = ['id']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []
