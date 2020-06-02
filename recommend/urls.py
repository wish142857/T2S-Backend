from django.urls import path
from . import views

urlpatterns = [
    path('recommend_fit_teacher', views.recommend_fit_teacher, name='recommend_fit_teacher'),
    path('recommend_hot_teacher', views.recommend_hot_teacher, name='recommend_hot_teacher'),
    path('recommend_random_teacher', views.recommend_random_teacher, name='recommend_random_teacher'),
    path('recommend_fit_student', views.recommend_fit_student, name='recommend_fit_student'),
    path('recommend_hot_student', views.recommend_hot_student, name='recommend_hot_student'),
    path('recommend_random_student', views.recommend_random_student, name='recommend_random_student'),
]
