from django.urls import path
from .views import index, article

urlpatterns = [
    path('', index, name="news_index"),  # Renommer l'URL pour éviter les conflits
    path('article/<int:number_article>/', article, name="article"),
]