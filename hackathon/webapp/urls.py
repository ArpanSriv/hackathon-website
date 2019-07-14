from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registration, name='registration'),
    path('register/individual', views.registration_individual, name='registration_individual'),
    path('register/startup', views.registration_startup, name='registration_startup'),
    path('register/privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('register/about_us', views.about_us, name='about_us'),
]