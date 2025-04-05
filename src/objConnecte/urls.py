from django.urls import path
from . import views
from .views import update_coordinates

app_name = 'objConnecte'
urlpatterns = [
    path('', views.index, name='obj-index'),
    path('objets/', views.objets, name='objets'),
    path('objet/<int:id>/', views.objet, name='objet'),
    path('api/toggle-state/<int:id>/', views.toggle_state, name='toggle_state'),
    path('api/refresh-state/<int:id>/', views.refresh_state, name='refresh_state'),
    path('api/delete-object/<int:id>/', views.delete_object, name='delete_object'),
    path('api/toggle-highlight/<int:id>/', views.toggle_highlight, name='toggle_highlight'),
    path('create/', views.create_object, name='create_object'),
    path('edit/<int:id>/', views.edit_object, name='edit_object'),
    path('api/update-coordinates/<int:id>/', update_coordinates, name='update_coordinates'),
    path('reports/', views.object_reports, name='reports'),
    path('reports/<int:id>/', views.object_reports, name='object_reports'),
    path('reports/export/<str:format>/', views.export_report, name='export_report'),
    path('reports/<int:id>/export/<str:format>/', views.export_report, name='export_object_report'),
]

