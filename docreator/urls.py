from django.urls import path

from docreator.views import CreateDocumentInstanceView, DeleteDocumentInstanceView, CreateDocumentTemplateView, DeleteDocumentTemplateView, IndexView


app_name = 'docreator'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('template/create/', CreateDocumentTemplateView.as_view(), name='create-template'),
    path('template/delete/', DeleteDocumentTemplateView.as_view(), name='delete-template'),
    path('instance/create/', CreateDocumentInstanceView.as_view(), name='create-instance'),
    path('instance/delete/', DeleteDocumentInstanceView.as_view(), name='delete-instance'),
]
