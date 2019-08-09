from django.urls import path
from django.views.generic import TemplateView

from solutions.views import FilePolicyAPI, FileUploadCompleteHandler
from . import views

urlpatterns = [
    # path('login', views.login_solution, name='login'),
    # path('upload_solution', views.upload_solution, name='upload_solution')
    path('upload/', TemplateView.as_view(template_name='upload.html'), name='upload-home'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),
    path('api/files/policy/', FilePolicyAPI.as_view(), name='upload-policy'),
	#path('login/', TemplateView.as_view(template_name='upload_login.html'), name='upload_login'),    
]
