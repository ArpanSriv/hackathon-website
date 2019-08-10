from django.urls import path
from django.views.generic import TemplateView

from solutions.views import FilePolicyAPI, FileUploadCompleteHandler
from . import views

urlpatterns = [
    path('login', TemplateView.as_view(template_name='solutions/upload_login.html'), name='login'),
    # path('upload_solution', views.upload_solution, name='upload_solution'),
    path('upload/', TemplateView.as_view(template_name='upload.html'), name='upload-home'),
    path('api/files/policy/', FilePolicyAPI.as_view(), name='upload-policy'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),
]
