from django.urls import path
from . import views

urlpatterns = [
    path('recommend_teacher', views.recommend_teacher, name='recommend_teacher'),
    path('recommend_student', views.recommend_student, name='recommend_student'),
]
