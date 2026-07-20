from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("worship/", views.schedule, name="schedule"),
    path("new-here/", views.new_here, name="new_here"),
    path("ministries/", views.ministries, name="ministries"),
    path("ministries/<slug:slug>/", views.ministry_detail, name="ministry_detail"),
    path("events/", views.events, name="events"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("sermons/", views.sermons, name="sermons"),
    path("livestream/", views.livestream, name="livestream"),
    path("sacraments/", views.sacraments, name="sacraments"),
    path("give/", views.give, name="give"),
    path("contact/", views.contact, name="contact"),
]
