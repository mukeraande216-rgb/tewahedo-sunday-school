from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('create/', views.calendar_event_create, name='calendar_event_create'),
    path('<int:event_id>/edit/', views.calendar_event_edit, name='calendar_event_edit'),
    path('<int:event_id>/delete/', views.calendar_event_delete, name='calendar_event_delete'),
]