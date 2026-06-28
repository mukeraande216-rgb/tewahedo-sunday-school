from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('take/', views.take_attendance, name='take_attendance'),
]