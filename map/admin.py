from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "x", "y", "width", "height", "floor")
    list_filter = ("floor",)
    search_fields = ("name", "code")
