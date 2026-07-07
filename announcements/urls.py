from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('create/', views.announcement_create, name='announcement_create'),
    path('<int:announcement_id>/edit/', views.announcement_edit, name='announcement_edit'),
    path('<int:announcement_id>/delete/', views.announcement_delete, name='announcement_delete'),
    path('<int:announcement_id>/repost/', views.announcement_repost, name='announcement_repost'),
]