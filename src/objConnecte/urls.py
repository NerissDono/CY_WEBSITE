from django.urls import path
from . import views

app_name = 'objConnecte'
urlpatterns = [
    path('', views.index, name='obj-index'),
    path('objets/', views.objets, name='objets'),
    path('objet/<int:id>/', views.objet, name='objet'),
]

