from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('animais/', views.animal_list, name='animal_list'),
    path('animais/novo/', views.animal_create, name='animal_create'),
    path('adotantes/', views.adotante_list, name='adotante_list'),
    path('adotantes/novo/', views.adotante_create, name='adotante_create'),
    path('contato/', views.contact, name='contact'),
]
