from django.urls import path
from . import views

urlpatterns = [
    path('get_watchlist', views.get_watchlist, name='get_watchlist'),
    path('get_fanlist', views.get_fanlist, name='get_fanlist'),
    path('add_to_watch', views.add_to_watch, name='add_to_watch'),
    path('delete_from_watch', views.delete_from_watch, name='delete_from_watch'),
]
