from django.db import migrations

ROOMS = [
    {
        "name": "Переговорная",
        "code": "MEET-01",
        "coordinates": "30,30 230,30 230,200 30,200",
        "label_x": 130,
        "label_y": 115,
        "fill_color": "#f0f4ff",
    },
    {
        "name": "Комната для преподавателей",
        "code": "TEACH-01",
        "coordinates": "30,200 230,200 230,370 30,370",
        "label_x": 130,
        "label_y": 285,
        "fill_color": "#fef3e2",
    },
    {
        "name": "Обеденная зона",
        "code": "DINE-01",
        "coordinates": "230,30 500,30 500,200 230,200",
        "label_x": 365,
        "label_y": 115,
        "fill_color": "#e8f5e9",
    },
    {
        "name": "Лаунж",
        "code": "LOUNGE-01",
        "coordinates": "230,200 500,200 500,370 230,370",
        "label_x": 365,
        "label_y": 285,
        "fill_color": "#fce4ec",
    },
    {
        "name": "Кухня",
        "code": "KIT-01",
        "coordinates": "500,30 690,30 690,200 500,200",
        "label_x": 595,
        "label_y": 115,
        "fill_color": "#e0f7fa",
    },
    {
        "name": "Санузел (муж.)",
        "code": "WC-M",
        "coordinates": "500,200 690,200 690,285 500,285",
        "label_x": 595,
        "label_y": 242,
        "fill_color": "#f5f5f5",
    },
    {
        "name": "Санузел (жен.)",
        "code": "WC-W",
        "coordinates": "500,285 690,285 690,370 500,370",
        "label_x": 595,
        "label_y": 327,
        "fill_color": "#f5f5f5",
    },
    {
        "name": "Архив",
        "code": "ARCH-01",
        "coordinates": "690,30 970,30 970,190 690,190",
        "label_x": 830,
        "label_y": 110,
        "fill_color": "#ede7f6",
    },
    {
        "name": "Коммуникационный отдел",
        "code": "COMMS-01",
        "coordinates": "230,370 473,370 473,570 230,570",
        "label_x": 351,
        "label_y": 470,
        "fill_color": "#e8eaf6",
    },
    {
        "name": "Проектный офис",
        "code": "PROJ-01",
        "coordinates": "473,370 716,370 716,570 473,570",
        "label_x": 594,
        "label_y": 470,
        "fill_color": "#fff3e0",
    },
    {
        "name": "Канцелярия / уч. отдел / Менеджеры",
        "code": "OFFICE-01",
        "coordinates": "716,370 970,370 970,570 716,570",
        "label_x": 843,
        "label_y": 470,
        "fill_color": "#e0f2f1",
    },
]


def seed(apps, schema_editor):
    Room = apps.get_model("map", "Room")
    for data in ROOMS:
        Room.objects.get_or_create(code=data["code"], defaults={**data, "floor": 1})


def unseed(apps, schema_editor):
    Room = apps.get_model("map", "Room")
    Room.objects.filter(code__in=[r["code"] for r in ROOMS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0002_room_label_x_room_label_y_alter_room_fill_color"),
    ]
    operations = [
        migrations.RunPython(seed, unseed),
    ]
