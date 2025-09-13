from django.contrib import messages


class ErrorMessageMixin:
    error_message = ''

    # noinspection PyUnresolvedReferences
    def form_valid(self, form):
        response = super().form_valid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data