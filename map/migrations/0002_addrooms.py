from django.db import migrations
from django.contrib.auth.hashers import make_password
# Массив данных полностью переписан под актуальные координаты и структуру вашей таблицы из PostgreSQL
ROOMS = [
    {
        "name": "Архив",
        "code": "ARCH-01",
        "height": 289,
        "width": 220,
        "x": 750,
        "y": 31,
    },
    {
        "name": "Канцелярия / уч. отдел / Менеджеры",
        "code": "OFFICE-01",
        "height": 200,
        "width": 254,
        "x": 519,
        "y": 470,
    },
    {
        "name": "Коммуникационный отдел",
        "code": "COMMS-01",
        "height": 200,
        "width": 243,
        "x": 31,
        "y": 470,
    },
    {
        "name": "Комната для преподавателей",
        "code": "TEACH-01",
        "height": 170,
        "width": 200,
        "x": 33,
        "y": 299,
    },
    {
        "name": "Кухня",
        "code": "KIT-01",
        "height": 170,
        "width": 190,
        "x": 558,
        "y": 30,
    },
    {
        "name": "Лаунж",
        "code": "LOUNGE-01",
        "height": 276,
        "width": 255,
        "x": 303,
        "y": 32,
    },
    {
        "name": "Переговорная",
        "code": "MEET-01",
        "height": 268,
        "width": 200,
        "x": 30,
        "y": 30,
    },
    {
        "name": "Проектный офис",
        "code": "PROJ-01",
        "height": 200,
        "width": 243,
        "x": 274,
        "y": 471,
    },
    {
        "name": "Санузел (жен.)",
        "code": "WC-W",
        "height": 85,
        "width": 122,
        "x": 438,
        "y": 309,
    },
    {
        "name": "Санузел (муж.)",
        "code": "WC-M",
        "height": 85,
        "width": 138,
        "x": 301,
        "y": 309,
    },
]


def seed(apps, schema_editor):
    Room = apps.get_model("map", "Room")
    for data in ROOMS:
        # get_or_create обновит/создаст записи на основе новой структуры полей x, y, width, height
        Room.objects.get_or_create(code=data["code"], defaults={**data, "floor": 1})


def unseed(apps, schema_editor):
    Room = apps.get_model("map", "Room")
    Room.objects.filter(code__in=[r["code"] for r in ROOMS]).delete()

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User') 

    username = "admin"
    email = "admin@admin.com"
    password = "admin"

    if not User.objects.filter(username=username).exists():
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_staff=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0001_initial"),
        ("auth", "__latest__"),
    ]
    operations = [
        migrations.RunPython(seed, unseed),
        migrations.RunPython(create_superuser),
    ]