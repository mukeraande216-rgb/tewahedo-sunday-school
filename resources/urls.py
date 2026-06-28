from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('create/', views.resource_create, name='resource_create'),
    path('<int:resource_id>/edit/', views.resource_edit, name='resource_edit'),
    path('<int:resource_id>/delete/', views.resource_delete, name='resource_delete'),
]