from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/rooms/", views.rooms_api, name="rooms_api"),
]
