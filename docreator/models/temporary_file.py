import datetime

from django.contrib.sessions.backends.base import SessionBase
from django.db.models import DateTimeField, FileField, Manager, Model
from django.utils import timezone


class TemporaryFileManager(Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        actual = queryset.filter(expiry__gte=timezone.now())
        queryset.difference(actual).delete()
        return actual


def expiry_in_20_min():
    return timezone.now() + datetime.timedelta(minutes=20)


def temporary_files_storage(temp, filename):
    expiry_timestamp = int(temp.expiry.timestamp())
    return f'temp/{expiry_timestamp}.{filename}'


class TemporaryFile(Model):
    class Meta:
        verbose_name = 'Временный файл'
        verbose_name_plural = 'Временные файлы'

    file = FileField(upload_to=temporary_files_storage)
    expiry = DateTimeField(default=expiry_in_20_min)

    def __str__(self):
        return f'temp:{self.file.path}'

    @classmethod
    def get_from_session(cls, session: SessionBase):
        try: return cls.objects.get(id=session['temp_id'])
        except: return 404

    @classmethod
    def delete_from_session(cls, session: SessionBase):
        cls.objects.filter(id=session.get('temp_id', -1)).delete()
