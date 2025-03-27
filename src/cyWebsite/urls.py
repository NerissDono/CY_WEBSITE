from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cyWebsite'
urlpatterns = [
    path('', views.index, name='index'),
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('objets_connectés/', include('objConnecte.urls')),
    path('user/', include('user.urls')),
]
