from django.urls import path
from . import views
from .views import delete_article, mark_as_read

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
    path('make-admin/', views.temp_make_admin, name='make_admin'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('mark_as_read/<int:article_id>/', mark_as_read, name='mark_as_read'),
]




