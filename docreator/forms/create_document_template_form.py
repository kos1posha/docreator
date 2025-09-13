import os.path

from django.forms import CharField, ModelChoiceField, ModelForm
from django.forms.utils import ErrorList
from docxtpl import DocxTemplate

from docreator.models import DocumentTemplate, Field, FieldType


class CreateDocumentTemplateForm(ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'description']

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance, use_required_attribute, renderer)
        self.file = files['file']
        self.jinja_fields = []
        self.template_fields = []
        self.init_template_fields()

    @property
    def filename(self):
        with_expiry = os.path.basename(self.file.path)
        return '.'.join(with_expiry.split('.')[1:])

    def save(self, commit=True):
        template = super().save(False)
        fields = {}
        for name_in_template in self.jinja_fields:
            fields[name_in_template] = Field(
                name_in_template=name_in_template,
                type=self.cleaned_data.get(f'{name_in_template}__type'),
                label=self.cleaned_data.get(f'{name_in_template}__label'),
                help_text=self.cleaned_data.get(f'{name_in_template}__help_text'),
                default=self.cleaned_data.get(f'{name_in_template}__default')
            )
        return template, fields

    def init_template_fields(self):
        docx = DocxTemplate(self.file.path)
        for name_in_template in sorted(docx.undeclared_template_variables):
            self.jinja_fields.append(name_in_template)
            self.template_fields.append(self.build_template_field(name_in_template))

    def build_template_field(self, name_in_template):
        self.fields[f'{name_in_template}__type'] = type = ModelChoiceField(queryset=FieldType.objects.exclude(pk=1), initial=2, empty_label=None, required=False)
        self.fields[f'{name_in_template}__label'] = label = CharField(max_length=60, required=False)
        self.fields[f'{name_in_template}__help_text'] = help_text = CharField(max_length=120, required=False)
        self.fields[f'{name_in_template}__default'] = default = CharField(max_length=600, required=False)
        return {'name_in_template': name_in_template, 'type': type, 'label': label, 'help_text': help_text, 'default': default}
