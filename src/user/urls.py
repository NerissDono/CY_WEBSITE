from django.urls import path
from .views import login_user, logout_user, password_reset_request, register_user, change_password, update_profile_picture, update_user_xp_level

app_name = 'user'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('change_password/', change_password, name='change_password'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
    path('update_xp/<str:username>/<str:new_level>/', update_user_xp_level, name='update_xp_level'),
]
