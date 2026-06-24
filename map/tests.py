import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Room


class RoomModelTest(TestCase):
    def test_create_room(self):
        room = Room.objects.create(
            name="Тестовая комната",
            code="TST-ROOM-01",
            x=30,
            y=30,
            width=200,
            height=170,
            floor=1,
        )
        self.assertEqual(room.name, "Тестовая комната")
        self.assertEqual(room.code, "TST-ROOM-01")
        self.assertEqual(room.x, 30)
        self.assertEqual(room.y, 30)
        self.assertEqual(room.width, 200)
        self.assertEqual(room.height, 170)
        self.assertEqual(room.floor, 1)

    def test_default_values(self):
        room = Room.objects.create(name="Тест", code="TST-DEFAULT-01")
        self.assertEqual(room.x, 0)
        self.assertEqual(room.y, 0)
        self.assertEqual(room.width, 100)
        self.assertEqual(room.height, 100)
        self.assertEqual(room.floor, 1)

    def test_str_representation(self):
        room = Room.objects.create(name="Серверная", code="SRV-01")
        self.assertEqual(str(room), "Серверная (SRV-01)")

    def test_unique_code(self):
        Room.objects.create(name="A", code="UNIQUE-TEST")
        with self.assertRaises(Exception):
            Room.objects.create(name="B", code="UNIQUE-TEST")

    def test_ordering(self):
        Room.objects.create(name="B", code="ORD-B")
        Room.objects.create(name="A", code="ORD-A")
        rooms = Room.objects.all()
        self.assertEqual(rooms[0].code, "ORD-A")
        self.assertEqual(rooms[1].code, "ORD-B")


class HomePageTest(TestCase):
    def test_status_200(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)

    def test_rooms_in_context(self):
        resp = self.client.get(reverse("home"))
        self.assertIn("rooms", resp.context)
        self.assertGreaterEqual(len(resp.context["rooms"]), 1)

    def test_rooms_json_in_context(self):
        resp = self.client.get(reverse("home"))
        self.assertIn("rooms_json", resp.context)
        data = json.loads(resp.context["rooms_json"])
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("name", data[0])
        self.assertIn("code", data[0])

    def test_template_used(self):
        resp = self.client.get(reverse("home"))
        self.assertTemplateUsed(resp, "map/index.html")


class SaveRoomsAPITest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name="Тест", code="API-TST-01", x=10, y=10, width=100, height=100
        )
        self.staff, _ = User.objects.get_or_create(
            username="api-staff", defaults={"is_staff": True},
        )
        self.staff.set_password("pass")
        self.staff.save()
        self.user, _ = User.objects.get_or_create(
            username="api-user", defaults={"is_staff": False},
        )
        self.user.set_password("pass")
        self.user.save()

    def test_staff_can_save(self):
        self.client.login(username="api-staff", password="pass")
        payload = {
            "rooms": [
                {"id": self.room.id, "x": 50, "y": 60, "width": 120, "height": 130}
            ]
        }
        resp = self.client.post(
            reverse("save_rooms"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["updated"], 1)
        self.room.refresh_from_db()
        self.assertEqual(self.room.x, 50)
        self.assertEqual(self.room.y, 60)
        self.assertEqual(self.room.width, 120)
        self.assertEqual(self.room.height, 130)

    def test_anon_cannot_save(self):
        payload = {
            "rooms": [
                {"id": self.room.id, "x": 50, "y": 60, "width": 120, "height": 130}
            ]
        }
        resp = self.client.post(
            reverse("save_rooms"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json()["status"], "error")

    def test_non_staff_cannot_save(self):
        self.client.login(username="api-user", password="pass")
        payload = {
            "rooms": [
                {"id": self.room.id, "x": 50, "y": 60, "width": 120, "height": 130}
            ]
        }
        resp = self.client.post(
            reverse("save_rooms"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json()["status"], "error")

    def test_save_multiple_rooms(self):
        r2 = Room.objects.create(name="R2", code="API-MULTI-01", x=0, y=0, width=50, height=50)
        self.client.login(username="api-staff", password="pass")
        payload = {
            "rooms": [
                {"id": self.room.id, "x": 10, "y": 20, "width": 30, "height": 40},
                {"id": r2.id, "x": 50, "y": 60, "width": 70, "height": 80},
            ]
        }
        resp = self.client.post(
            reverse("save_rooms"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["updated"], 2)

    def test_invalid_json_returns_400(self):
        self.client.login(username="api-staff", password="pass")
        resp = self.client.post(
            reverse("save_rooms"),
            data="not json",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
