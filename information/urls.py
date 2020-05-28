from django.urls import path
from . import views

urlpatterns = [
    path('get_information', views.get_information, name='get_information'),
    path('get_information_detail', views.get_information_detail, name='get_information_detail'),
    path('set_information_state', views.set_information_state, name='set_information_state'),
    path('create_information', views.create_information, name='create_information'),
    path('delete_information', views.delete_information, name='delete_information'),
    path('update_information', views.update_information, name='update_information'),
]
