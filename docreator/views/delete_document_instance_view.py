from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from docreator.models import DocumentInstance


class DeleteDocumentInstanceView(View):
    success_url = reverse_lazy('users:profile')
    success_message = 'Экземпляр успешно удален'

    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        instance_id = self.request.POST.get('instance-id')
        instance = DocumentInstance.objects.filter(id=instance_id, template__user=request.user).first()
        if instance:
            instance.delete()
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
