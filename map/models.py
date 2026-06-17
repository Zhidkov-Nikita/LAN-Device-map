from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код комнаты")
    coordinates = models.TextField(verbose_name="SVG-путь (polygon points)")
    label_x = models.PositiveSmallIntegerField(default=0, verbose_name="Позиция названия X")
    label_y = models.PositiveSmallIntegerField(default=0, verbose_name="Позиция названия Y")
    floor = models.PositiveSmallIntegerField(default=1, verbose_name="Этаж")
    fill_color = models.CharField(max_length=7, default="#f8f8f8", verbose_name="Цвет заливки")

    class Meta:
        ordering = ["floor", "name"]
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return f"{self.name} ({self.code})"
