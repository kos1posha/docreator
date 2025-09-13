from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from docreator.models import DocumentInstance, DocumentTemplate


class CreateDocumentInstanceView(SuccessMessageMixin, View):
    success_url = reverse_lazy('users:profile')
    success_message = 'Экземпляр успешно создан'

    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        values = {field: value for field, value in self.request.POST.items() if field not in ['csrfmiddlewaretoken', 'encoding', 'template-id']}
        template = DocumentTemplate.objects.filter(id=self.request.POST.get('template-id', '-1')).first()
        if template is None:
            messages.error(request, 'При создании экземпляра произошла ошибка')
            return redirect('users:profile')
        instance = DocumentInstance(template=template)
        instance.save(instance_values=values)
        return redirect('users:profile')
