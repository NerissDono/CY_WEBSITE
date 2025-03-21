from django.urls import path, include
from .views import index, article

urlpatterns = [
    path('',index,name="index"),
    #path('article <int : article_number>',article,include('news.urls')),
]