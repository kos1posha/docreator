from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings
from users.api import ApiRouter, UserViewSet


urlpatterns = [
    path('django/admin/', admin.site.urls),

    path('', include('docreator.urls', namespace='docreator')),
    path('', include('users.urls', namespace='users')),
]

router = ApiRouter()
router.register('users', UserViewSet)
api_name = 'api'
urlpatterns += [
    path(f'{api_name}/', include((router.urls, api_name), namespace='api')),
    path(f'{api_name}/sessions/', include('rest_framework.urls')),
    path(f'{api_name}/tokens/', include('users.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    for prefix, root in settings.STATICFILES_DIRS:
        static(f'{settings.STATIC_URL}{prefix}/',  document_root=root)
