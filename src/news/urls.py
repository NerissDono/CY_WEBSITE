from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('information/', views.information, name='information'),
    path('visualisation/', views.visualisation, name='visualisation'),
    path('gestion/', views.gestion, name='gestion'),
    path('administration/', views.administration, name='administration'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('connexion/', views.connexion, name='connexion'),
]




