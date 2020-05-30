from django.urls import path
from . import views

urlpatterns = [
    path('logon', views.logon, name='logon'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('user_auth', views.user_auth, name='user_auth'),
    path('change_password', views.change_password, name='change_password'),

    path('get_info', views.get_info, name='get_info'),
    path('update_info', views.update_info, name='update_info'),
    path('get_info_plus', views.get_info_plus, name='get_info_plus'),
    path('update_info_plus', views.update_info_plus, name='update_info_plus'),
    path('get_info_picture', views.get_info_picture, name='get_info_picture'),
    path('update_info_picture', views.update_info_picture, name='update_info_picture'),
]