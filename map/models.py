from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код комнаты")
    x = models.IntegerField(default=0, verbose_name="Координата X")
    y = models.IntegerField(default=0, verbose_name="Координата Y")
    width = models.IntegerField(default=100, verbose_name="Ширина")
    height = models.IntegerField(default=100, verbose_name="Высота")
    floor = models.PositiveSmallIntegerField(default=1, verbose_name="Этаж")

    class Meta:
        ordering = ["floor", "name"]
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return f"{self.name} ({self.code})"
