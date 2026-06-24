from django.contrib import admin

from .models import Room

admin.site.site_header = "LAN Device Map Administration"
admin.site.site_title = "LAN Device Map Admin"
admin.site.index_title = "Добро пожаловать в панель управления LAN Device Map"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "x", "y", "width", "height", "floor")
    list_filter = ("floor",)
    search_fields = ("name", "code")
