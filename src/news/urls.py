from django.urls import path
from . import views
from .views import delete_article

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    path('information/', views.information, name='information'),
    path('visualisation/', views.visualisation, name='visualisation'),
    path('gestion/', views.gestion, name='gestion'),
    path('administration/', views.administration, name='administration'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('connexion/', views.connexion, name='connexion'),
    path('create_article/', views.create_article, name='create_article'),  # Nouveau chemin
    path('my_articles/', views.my_articles, name='my_articles'),  # Nouveau chemin
    path('delete_article/<int:article_id>/', delete_article, name='delete_article'),
]




