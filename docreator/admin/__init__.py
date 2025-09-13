from django.contrib import admin

from .document_instance_admin import DocumentInstanceAdmin
from .document_template_admin import DocumentTemplateAdmin
from .field_admin import FieldAdmin
from .field_type_admin import FieldTypeAdmin
from .value_admin import ValueAdmin
from ..models import DocumentInstance, DocumentTemplate, Field, FieldType, Value


admin.site.register(DocumentInstance, DocumentInstanceAdmin)
admin.site.register(DocumentTemplate, DocumentTemplateAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(FieldType, FieldTypeAdmin)
admin.site.register(Value, ValueAdmin)
