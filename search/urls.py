from django.urls import path
from . import views

urlpatterns = [
    path('search_teacher', views.search_teacher, name='search_teacher'),
    path('search_student', views.search_student, name='search_student'),
    path('search_recruit_intention', views.search_recruit_intention, name='search_recruit_intention'),
    path('search_apply_intention', views.search_apply_intention, name='search_apply_intention'),
]
