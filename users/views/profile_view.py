from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
import requests
import requests.auth
from rest_framework import status


def send_request(url, auth, data):
    auth = requests.auth.HTTPBasicAuth(*auth)
    response = requests.patch(url, data, auth=auth)
    return response


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def post(self, request: WSGIRequest, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        url = request.build_absolute_uri(reverse('api:user-detail', kwargs={'pk': request.user.id}))
        auth = (request.user.username, request.POST.get('password-confirm', ''))
        if 'new-username' in request.POST:
            new_username = request.POST.get('new-username', '')
            changed = ('username', new_username)
            success_message, init_tab, light_refresh = 'Имя пользователя успешно изменено', 1, True
        elif 'new-email' in request.POST:
            new_email = request.POST.get('new-email', '')
            changed = ('email', new_email)
            success_message, init_tab, light_refresh = 'Адрес электронной почты успешно изменен', 1, True
        elif 'new-password1' in request.POST:
            new_password1, new_password2 = request.POST.get('new-password1', ''), request.POST.get('new-password2', '')
            if new_password1 != new_password2:
                context.update({'errors': {'password_confirm': ['Пароли не совпадают']}, 'init_tab': 2})
                return render(request, self.template_name, context)
            changed = ('password', make_password(new_password1))
            success_message, init_tab, light_refresh = 'Пароль успешно изменен. Войдите снова с новый паролем', 2, False
        else:
            return self.render_to_response(context)
        data = {changed[0]: changed[1]}
        response = send_request(url, auth, data)
        match response.status_code:
            case status.HTTP_200_OK:
                messages.success(request, success_message)
                if light_refresh:
                    setattr(request.user, *changed)
                else:
                    return redirect('docreator:index')
            case status.HTTP_400_BAD_REQUEST:
                context.update({'errors': response.json()})
            case status.HTTP_403_FORBIDDEN:
                messages.error(request, 'Указан неверный текущий пароль')
            case _:
                messages.error(request, f'[{response.status_code}] {response.reason} - {response.text}')
        context.update({'init_tab': init_tab})
        return render(request, self.template_name, context)
