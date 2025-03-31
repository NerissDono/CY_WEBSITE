from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_user, logout_user, password_reset_request, register_user, change_password, update_user, update_user_xp_level, search_user, public_profile, update_profile_picture, activate_account

app_name = 'user'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('change_password/', change_password, name='change_password'),
    path('update_user/', update_user, name='update_user'),
    path('update_xp/<str:username>/<str:new_level>/', update_user_xp_level, name='update_xp_level'),
    path('search_user/', search_user, name='search_user'),
    path('profile/<str:username>/', public_profile, name='public_profile'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
]
