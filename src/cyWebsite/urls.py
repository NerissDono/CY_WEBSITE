from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cyWebsite'
urlpatterns = [
    path('', views.index, name='index'),
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('objets_connectés/', include('objConnecte.urls')),
    path('user/', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
