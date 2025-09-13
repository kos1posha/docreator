from django.urls import reverse_lazy
from django.views.generic import FormView

from docreator.forms import FileChooseForm
from docreator.models import TemporaryFile


class IndexView(FormView):
    form_class = FileChooseForm
    template_name = 'docreator\index.html'
    success_url = reverse_lazy(f'docreator:create-template')

    def form_valid(self, form):
        TemporaryFile.delete_from_session(self.request.session)
        temp = form.save()
        self.request.session['temp_id'] = temp.id
        return super().form_valid(form)
