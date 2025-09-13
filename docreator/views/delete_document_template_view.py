from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from docreator.models import DocumentTemplate


class DeleteDocumentTemplateView(SuccessMessageMixin, View):
    success_url = reverse_lazy('users:profile')
    success_message = 'Шаблон успешно удален'

    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        template_id = self.request.POST.get('template-id')
        template = DocumentTemplate.objects.filter(id=template_id, user=request.user).first()
        if template:
            template.delete()
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
