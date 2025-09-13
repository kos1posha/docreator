import os.path

from django.apps import apps
from django.db.models import CASCADE, CharField, DateTimeField, FileField, ForeignKey, Model
from django.utils import timezone as tz
from django.utils.formats import date_format
from docxtpl import DocxTemplate

from core.settings import BASE_DIR, MEDIA_ROOT
from docreator.models.field import Field
from docreator.models.value import Value


class DocumentInstance(Model):
    class Meta:
        verbose_name = 'Экземпляр документа'
        verbose_name_plural = 'Экземпляры документов'

    template = ForeignKey(
        verbose_name='Шаблон',
        to='docreator.DocumentTemplate',
        on_delete=CASCADE,
    )
    name = CharField(
        verbose_name='Название',
        max_length=60,
        blank=True,
        null=True,
    )
    created = DateTimeField(
        verbose_name='Создан',
        auto_now_add=True,
    )
    modified = DateTimeField(
        verbose_name='Последнее изменение',
        auto_now=True,
        blank=True,
        null=True,
    )
    content = FileField(
        verbose_name='Файл шаблона',
        upload_to='instances/',
    )

    def __str__(self):
        return f'Экземпляр "{self.full_name}" от {date_format(tz.localtime(self.created))}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, instance_values=None):
        instance_values = instance_values or {}
        creating = not apps.get_model('docreator.DocumentInstance').objects.filter(pk=self.pk).exists()
        super().save(force_insert, force_update, using, update_fields)
        if creating:
            for field in self.template.jinja_fields:
                field_model = Field.objects.get(template=self.template, name_in_template=field)
                value_model = Value(instance=self, field=field_model)
                value_model.value = instance_values.get(field, '')
                value_model.save(force_insert, force_update, using, update_fields)
            content_name = f'instances/{self.user.username}/{self.id}.{self.safe_name}.{self.template.file}'
            content_path = BASE_DIR / MEDIA_ROOT / content_name
            content_dir = os.path.dirname(content_path)
            if not os.path.exists(content_dir):
                os.makedirs(content_dir)
            docx = DocxTemplate(self.template.content.path)
            docx.render(instance_values)
            docx.save(content_path)
            self.content.name = content_name
            super().save(force_insert, force_update, using, update_fields)

    @property
    def safe_name(self):
        return self.name or 'Без названия'

    @property
    def full_name(self):
        return f'{self.template.safe_name} : {self.safe_name}'

    @property
    def user(self):
        return self.template.user

    @property
    def values(self):
        return Value.objects.filter(instance=self)
