from django.db.models import CASCADE, CharField, ForeignKey, Model, TextField, UniqueConstraint
from django.utils.safestring import mark_safe


def datetime_format():
    return '%Y-%m-%d %H:%M:%S.%f'


class Field(Model):
    class Meta:
        verbose_name = 'Поле шаблона'
        verbose_name_plural = 'Поля шаблонов'
        constraints = [
            UniqueConstraint(fields=['template', 'name_in_template'], name='unique_name_in_template_constraint')
        ]

    template = ForeignKey(
        verbose_name='Шаблон',
        to='docreator.DocumentTemplate',
        on_delete=CASCADE,
    )
    name_in_template = CharField(
        verbose_name='Название в шаблоне',
        max_length=30,
    )
    type = ForeignKey(
        verbose_name='Тип',
        to='docreator.FieldType',
        on_delete=CASCADE,
        default=2,
    )
    label = CharField(
        verbose_name='Подпись',
        max_length=60,
        blank=True,
        null=True,
    )
    help_text = TextField(
        verbose_name='Вспомогательный текст',
        max_length=120,
        blank=True,
        null=True,
    )
    default = CharField(
        verbose_name='Значение по умолчанию',
        max_length=600,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Поле {self.tag} шаблона "{self.template.safe_name}"'

    @property
    def tag(self):
        return f'{{{{ {self.name_in_template} }}}}'

    @property
    def input_attrs(self):
        attrs = {}
        match self.type.code:
            case 'str':
                attrs['type'] = 'text'
            case 'int':
                attrs['type'] = 'number'
                attrs['step'] = '1'
            case 'float':
                attrs['type'] = 'number'
                attrs['step'] = '0.1'
            case 'datetime':
                attrs['type'] = 'datetime-local'
            case 'date' | 'time' | 'email':
                attrs['type'] = self.type.code
            case _:
                attrs['type'] = 'text'
        return mark_safe(' '.join([f'{attr}="{value}"' for attr, value in attrs.items()]))
