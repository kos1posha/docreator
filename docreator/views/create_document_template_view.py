import os.path
import shutil

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from core import settings
from docreator.forms import CreateDocumentTemplateForm
from docreator.models import TemporaryFile


class CreateDocumentTemplateView(SuccessMessageMixin, FormView):
    form_class = CreateDocumentTemplateForm
    template_name = 'docreator/create_template.html'
    success_message = 'Шаблон успешно создан'
    success_url = reverse_lazy('docreator:index')

    def get(self, request, *args, **kwargs):
        temp = TemporaryFile.get_from_session(self.request.session)
        if temp == 404:
            return redirect('docreator:index')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        temp = TemporaryFile.get_from_session(self.request.session)
        kwargs = super().get_form_kwargs()
        kwargs['files'] = {'file': temp.file}
        return kwargs

    def form_valid(self, form):
        template, fields = form.save()
        template.user = self.request.user
        content_name = f'docx/{self.request.user.username}/{form.filename}'
        shutil.copyfile(form.file.path, f'{os.path.join(settings.MEDIA_ROOT, content_name)}')
        template.content.name = content_name
        template.save(template_fields=fields)
        TemporaryFile.delete_from_session(self.request.session)
        return super().form_valid(form)
