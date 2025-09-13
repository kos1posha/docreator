from django.db.models import Model, CharField, TextField


class FieldType(Model):
    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'

    code = CharField(
        'Код',
        max_length=8,
        unique=True,
    )
    name = CharField(
        'Название',
        max_length=30,
        unique=True,
    )
    description = TextField(
        'Описание',
        max_length=600,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.code}'
