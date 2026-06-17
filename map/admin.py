from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "floor")
    list_filter = ("floor",)
    search_fields = ("name", "code")
