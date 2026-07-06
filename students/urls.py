from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('enroll/', views.student_enroll_class, name='student_enroll_class'),
]