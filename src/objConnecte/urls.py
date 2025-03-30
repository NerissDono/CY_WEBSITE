from django.urls import path
from . import views

app_name = 'objConnecte'
urlpatterns = [
    path('', views.index, name='obj-index'),
    path('objets/', views.objets, name='objets'),
    path('objet/<int:id>/', views.objet, name='objet'),
    path('api/toggle-state/<int:id>/', views.toggle_state, name='toggle_state'),
    path('api/refresh-state/<int:id>/', views.refresh_state, name='refresh_state'),
    path('api/delete-object/<int:id>/', views.delete_object, name='delete_object'),  # Nouvelle URL
]

