from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('create/', views.message_create, name='message_create'),
    path('<int:thread_id>/', views.message_detail, name='message_detail'),
    path('<int:thread_id>/close/', views.message_close, name='message_close'),
]