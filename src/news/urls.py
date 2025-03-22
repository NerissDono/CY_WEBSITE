from django.urls import path, include
from .views import index, article

urlpatterns = [
    path('',index,name='news_index'),
    #path('article <int : article_number>',article,include('news.urls')),
]