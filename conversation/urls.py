from django.urls import path
from . import views

urlpatterns = [
    path('get_conversation', views.get_conversation, name='get_conversation'),
    path('get_message', views.get_message, name='get_message'),
    path('get_new_messages', views.get_new_messages, name='get_new_messages'),
    path('get_all_messages', views.get_all_messages, name='get_all_messages'),
    path('get_message_detail', views.get_message_detail, name='get_message_detail'),
    path('get_message_picture', views.get_message_picture, name='get_message_picture'),
    path('send_message', views.send_message, name='send_message'),
]
