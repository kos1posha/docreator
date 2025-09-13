import os

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from docreator.models import TemporaryFile


class FileChooseForm(ModelForm):
    class Meta:
        model = TemporaryFile
        fields = ['file']

    error_messages = {
        'invalid_file_extension': 'Файл должен быть Word-документом (*.docx)',
    }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        ext = os.path.splitext(file.name)[1]
        if ext != '.docx':
            exc_code = 'invalid_file_extension'
            raise ValidationError(
                self.error_messages[exc_code],
                code=exc_code
            )
        return file
