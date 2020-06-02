from django.urls import path
from . import views

urlpatterns = [
    path('get_recruit_intention', views.get_recruit_intention, name='get_recruit_intention'),
    path('get_recruit_intention_detail', views.get_recruit_intention_detail, name='get_recruit_intention_detail'),
    path('get_recruit_intention_picture', views.get_recruit_intention_picture, name='get_recruit_intention_picture'),
    path('create_recruit_intention', views.create_recruit_intention, name='create_recruit_intention'),
    path('delete_recruit_intention', views.delete_recruit_intention, name='delete_recruit_intention'),
    path('update_recruit_intention', views.update_recruit_intention, name='update_recruit_intention'),

    path('get_apply_intention', views.get_apply_intention, name='get_apply_intention'),
    path('get_apply_intention_detail', views.get_apply_intention_detail, name='get_apply_intention_detail'),
    path('get_apply_intention_picture', views.get_apply_intention_picture, name='get_apply_intention_picture'),
    path('create_apply_intention', views.create_apply_intention, name='create_apply_intention'),
    path('delete_apply_intention', views.delete_apply_intention, name='delete_apply_intention'),
    path('update_apply_intention', views.update_apply_intention, name='update_apply_intention'),
]
