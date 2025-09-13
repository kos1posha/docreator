from django.db.models import CASCADE, CharField, ForeignKey, Model, UniqueConstraint
from django.utils import timezone as tz


class Value(Model):
    class Meta:
        verbose_name = 'Поле экземпляра'
        verbose_name_plural = 'Поля экземпляров'
        constraints = [
            UniqueConstraint(fields=['instance', 'field'], name='unique_name_in_instance_constraint')
        ]

    instance = ForeignKey(
        verbose_name='Экземпляр',
        to='docreator.DocumentInstance',
        on_delete=CASCADE,
    )
    field = ForeignKey(
        verbose_name='Поле',
        to='docreator.Field',
        on_delete=CASCADE,
    )
    value = CharField(
        verbose_name='Значение',
        max_length=1000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Значение {self.field.tag} экземпляра "{self.instance.full_name}"'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.instance.modified = tz.now()
        self.instance.save()

    @property
    def template(self):
        return self.instance.template

    @property
    def name_in_template(self):
        return self.field.name_in_template

    @property
    def type(self):
        return self.field.type
