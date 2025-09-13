import os.path

from django.apps import apps
from django.db.models import CASCADE, CharField, FileField, ForeignKey, Model, TextField
from django.forms import model_to_dict
from docxtpl import DocxTemplate

from docreator.models.document_instance import DocumentInstance
from docreator.models.field import Field


def docx_storage(docx, filename):
    return f'docx/{docx.user.username}/{filename}'


class DocumentTemplate(Model):
    class Meta:
        verbose_name = 'Шаблон документа'
        verbose_name_plural = 'Шаблоны документов'

    user = ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=CASCADE,
    )
    name = CharField(
        verbose_name='Название',
        max_length=60,
        blank=True,
        null=True,
    )
    description = TextField(
        verbose_name='Описание',
        max_length=600,
        blank=True,
        null=True,
    )
    content = FileField(
        verbose_name='Файл шаблона',
        upload_to=docx_storage,
    )

    def __str__(self):
        return f'Шаблон "{self.safe_name}"'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, fields_data=None, template_fields=None):
        template_fields = template_fields or {}
        creating = not apps.get_model('docreator.DocumentTemplate').objects.filter(pk=self.pk).exists()
        super().save(force_insert, force_update, using, update_fields)
        self._create(template_fields) if creating else self._update(template_fields)

    def _create(self, template_fields):
        for name_in_template in self.jinja_fields:
            field = template_fields.get(name_in_template, Field(name_in_template=name_in_template))
            field.template = self
            field.save()

    def _update(self, template_fields):
        for new in template_fields:
            old = Field.objects.filter(template=self, name_in_template=new.name_in_template)
            old.update(**model_to_dict(new, fields=['type', 'label', 'help_text', 'default']))
            old.first().save()

    @property
    def safe_name(self):
        return self.name or self.file

    @property
    def file(self):
        return os.path.basename(self.content.name)

    @property
    def jinja_fields(self):
        docx = DocxTemplate(self.content.path)
        return docx.undeclared_template_variables

    @property
    def instances(self):
        return DocumentInstance.objects.filter(template=self)

    @property
    def fields(self):
        return Field.objects.filter(template=self)
