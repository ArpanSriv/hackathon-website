from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_solution, name='login'),
    path('upload_solution', views.upload_solution, name='upload_solution')
]