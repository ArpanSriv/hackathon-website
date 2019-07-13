from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registration, name='registration'),
    path('register/individual', views.registration_individual, name='registration_individual'),
    path('register/startup', views.registration_startup, name='registration_startup')
]