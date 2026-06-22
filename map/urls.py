from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/rooms/", views.rooms_api, name="rooms_api"),
    path("api/rooms/save/", views.save_rooms, name="save_rooms"),
]
